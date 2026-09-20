#define _POSIX_C_SOURCE 200809L
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

static void msleep(long ms) {
    struct timespec ts = { .tv_sec = ms / 1000,
                           .tv_nsec = (ms % 1000) * 1000 * 1000 };
    nanosleep(&ts, NULL);
}
static volatile sig_atomic_t usr1_count = 0;
static volatile sig_atomic_t int_count = 0;

/* Async-signal-safe handler: only touches sig_atomic_t flags
 * and uses write(), never printf(). */
static void handler(int sig) {
    if (sig == SIGUSR1) usr1_count++;
    else if (sig == SIGINT) int_count++;
    const char m[] = "[handler] signal caught\n";
    (void)write(STDOUT_FILENO, m, sizeof(m) - 1);
}

int main(void) {
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;
    if (sigaction(SIGUSR1, &sa, NULL) != 0) { perror("sigaction USR1"); return 1; }
    if (sigaction(SIGINT, &sa, NULL) != 0)  { perror("sigaction INT");  return 1; }

    /* Ignore SIGPIPE explicitly to show disposition control. */
    signal(SIGPIPE, SIG_IGN);

    pid_t c = fork();
    if (c < 0) { perror("fork"); return 1; }
    if (c == 0) {
        /* Child sends 3x SIGUSR1 then 1x SIGINT to parent. */
        pid_t p = getppid();
        for (int i = 0; i < 3; i++) {
            msleep(100);
            if (kill(p, SIGUSR1) != 0) { perror("kill USR1"); _exit(1); }
        }
        msleep(100);
        if (kill(p, SIGINT) != 0) { perror("kill INT"); _exit(1); }
        _exit(0);
    }

    /* Parent waits until all 4 signals arrive (bounded loop => terminates). */
    for (int i = 0; i < 100; i++) { /* max ~10 s */
        if (usr1_count >= 3 && int_count >= 1) break;
        msleep(100);
    }
    int status = 0;
    waitpid(c, &status, 0);
    printf("[parent] SIGUSR1=%d SIGINT=%d child %s\n",
           (int)usr1_count, (int)int_count,
           (WIFEXITED(status) && WEXITSTATUS(status) == 0) ? "ok" : "FAILED");
    if (usr1_count == 3 && int_count == 1) {
        printf("[parent] OK: sigaction handlers work.\n");
        return 0;
    }
    fprintf(stderr, "[parent] FAIL: wrong signal counts.\n");
    return 1;
}
