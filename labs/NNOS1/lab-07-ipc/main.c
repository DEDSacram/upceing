#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

static void die(const char *m) { perror(m); exit(1); }

/* Demo 1: anonymous pipe, parent -> child, one message. */
static int demo_pipe(void) {
    int fd[2];
    if (pipe(fd) != 0) die("pipe");
    pid_t c = fork();
    if (c < 0) die("fork");
    if (c == 0) {
        close(fd[1]);
        char msg[128];
        ssize_t n = read(fd[0], msg, sizeof(msg) - 1);
        if (n < 0) die("read");
        msg[n] = '\0';
        printf("[pipe] child received: \"%s\"\n", msg);
        fflush(stdout);
        close(fd[0]);
        _exit(0);
    }
    close(fd[0]);
    const char *m = "hello through the pipe";
    if (write(fd[1], m, strlen(m)) < 0) die("write");
    close(fd[1]); /* EOF for the reader */
    int st = 0;
    waitpid(c, &st, 0);
    return WIFEXITED(st) && WEXITSTATUS(st) == 0;
}

/* Demo 2: socketpair, bidirectional: parent pings, child pongs. */
static int demo_socketpair(void) {
    int sv[2];
    if (socketpair(AF_UNIX, SOCK_STREAM, 0, sv) != 0) die("socketpair");
    pid_t c = fork();
    if (c < 0) die("fork");
    if (c == 0) {
        close(sv[0]);
        char msg[128];
        ssize_t n = read(sv[1], msg, sizeof(msg) - 1);
        if (n < 0) die("child read");
        msg[n] = '\0';
        printf("[socketpair] child received: \"%s\"\n", msg);
        fflush(stdout);
        const char *reply = "pong";
        if (write(sv[1], reply, strlen(reply)) < 0) die("child write");
        close(sv[1]);
        _exit(0);
    }
    close(sv[1]);
    const char *ping = "ping";
    if (write(sv[0], ping, strlen(ping)) < 0) die("parent write");
    char rep[128];
    ssize_t n = read(sv[0], rep, sizeof(rep) - 1);
    if (n < 0) die("parent read");
    rep[n] = '\0';
    printf("[socketpair] parent received: \"%s\"\n", rep);
    close(sv[0]);
    int st = 0, ok = (strcmp(rep, "pong") == 0);
    waitpid(c, &st, 0);
    ok = ok && WIFEXITED(st) && WEXITSTATUS(st) == 0;
    return ok;
}

int main(void) {
    int p1 = demo_pipe();
    int p2 = demo_socketpair();
    printf("pipe=%s socketpair=%s\n",
           p1 ? "OK" : "FAIL", p2 ? "OK" : "FAIL");
    return (p1 && p2) ? 0 : 1;
}
