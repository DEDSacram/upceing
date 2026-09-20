#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

/* fork/exec/wait demo:
 * - child 1: execs "echo" via execlp (replaces image)
 * - child 2: computes a sum and exits with a status code
 * - parent: waitpid() for both, prints exit statuses
 */
int main(void) {
    pid_t c1 = fork();
    if (c1 < 0) { perror("fork"); return 1; }
    if (c1 == 0) {
        printf("[child1] pid=%d ppid=%d: exec echo...\n", getpid(), getppid());
        fflush(stdout);
        execlp("echo", "echo", "hello from exec'd child1", (char *)NULL);
        perror("execlp"); /* only reached on error */
        _exit(127);
    }

    pid_t c2 = fork();
    if (c2 < 0) { perror("fork"); return 1; }
    if (c2 == 0) {
        long sum = 0;
        for (long i = 1; i <= 100; i++) sum += i;
        printf("[child2] pid=%d ppid=%d: sum(1..100)=%ld\n",
               getpid(), getppid(), sum);
        exit(42); /* exit status observed by parent */
    }

    printf("[parent] pid=%d waiting for %d and %d...\n",
           getpid(), (int)c1, (int)c2);
    int status, done = 0;
    while (done < 2) {
        pid_t w = wait(&status);
        if (w < 0) { perror("wait"); return 1; }
        if (WIFEXITED(status))
            printf("[parent] child %d exited, status=%d\n",
                   (int)w, WEXITSTATUS(status));
        else if (WIFSIGNALED(status))
            printf("[parent] child %d killed by signal %d\n",
                   (int)w, WTERMSIG(status));
        done++;
    }
    printf("[parent] all children reaped. No zombies.\n");
    return 0;
}
