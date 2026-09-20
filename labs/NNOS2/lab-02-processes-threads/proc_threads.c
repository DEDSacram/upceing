/* Linux try-out counterpart of Get-ProcessesThreads.ps1:
 * list own process info + threads of this process via /proc.
 * Compile: gcc -Wall -Wextra -pthread -o proc_threads proc_threads.c
 */
#define _GNU_SOURCE
#include <dirent.h>
#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

static void *worker(void *arg) {
    (void)arg;
    sleep(60); /* keep threads alive while main inspects /proc/self/task */
    return NULL;
}

int main(void) {
    pthread_t th[3];
    for (int i = 0; i < 3; i++)
        pthread_create(&th[i], NULL, worker, NULL);

    printf("pid=%d threads of this process (/proc/self/task):\n", getpid());
    DIR *d = opendir("/proc/self/task");
    if (!d) { perror("opendir"); return 1; }
    struct dirent *e;
    int n = 0;
    while ((e = readdir(d)) != NULL) {
        if (e->d_name[0] == '.') continue;
        char path[sizeof("/proc/self/task/") + 256 + sizeof("/comm")];
        char name[64] = "?";
        snprintf(path, sizeof(path), "/proc/self/task/%s/comm", e->d_name);
        FILE *f = fopen(path, "r");
        if (f) {
            if (fgets(name, sizeof(name), f))
                name[strcspn(name, "\n")] = '\0';
            fclose(f);
        }
        printf("  tid=%s comm=%s\n", e->d_name, name);
        n++;
    }
    closedir(d);
    printf("total threads=%d (expected >= 4): %s\n", n, n >= 4 ? "OK" : "FAIL");

    /* Priority class analogue: nice value of this process. */
    printf("pid=%d (Windows analogue: Get-Process -Id $PID | Select PriorityClass)\n",
           getpid());
    for (int i = 0; i < 3; i++) {
        pthread_cancel(th[i]);
        pthread_join(th[i], NULL);
    }
    return n >= 4 ? 0 : 1;
}
