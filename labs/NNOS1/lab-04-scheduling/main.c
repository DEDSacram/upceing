#define _GNU_SOURCE
#include <errno.h>
#include <sched.h>
#include <stdio.h>
#include <string.h>
#include <sys/resource.h>
#include <unistd.h>

static const char *pol_name(int p) {
    switch (p) {
    case SCHED_OTHER: return "SCHED_OTHER";
    case SCHED_FIFO:  return "SCHED_FIFO";
    case SCHED_RR:    return "SCHED_RR";
#ifdef SCHED_BATCH
    case SCHED_BATCH: return "SCHED_BATCH";
#endif
#ifdef SCHED_IDLE
    case SCHED_IDLE:  return "SCHED_IDLE";
#endif
#ifdef SCHED_DEADLINE
    case SCHED_DEADLINE: return "SCHED_DEADLINE";
#endif
    default: return "?";
    }
}

int main(void) {
    printf("pid=%d\n", getpid());

    /* 1. Current policy + priority. */
    int pol = sched_getscheduler(0);
    struct sched_param sp;
    sched_getparam(0, &sp);
    printf("policy=%s priority=%d\n", pol_name(pol), sp.sched_priority);
    printf("SCHED_OTHER min/max=%d/%d  FIFO min/max=%d/%d  RR min/max=%d/%d\n",
           sched_get_priority_min(SCHED_OTHER), sched_get_priority_max(SCHED_OTHER),
           sched_get_priority_min(SCHED_FIFO),  sched_get_priority_max(SCHED_FIFO),
           sched_get_priority_min(SCHED_RR),    sched_get_priority_max(SCHED_RR));

    /* 2. nice value: read, bump by +5 (lower our priority), read back. */
    errno = 0;
    int n0 = getpriority(PRIO_PROCESS, 0);
    printf("nice before=%d\n", n0);
    if (setpriority(PRIO_PROCESS, 0, n0 + 5) != 0) {
        perror("setpriority");
        return 1;
    }
    int n1 = getpriority(PRIO_PROCESS, 0);
    printf("nice after=%d (expected %d): %s\n",
           n1, n0 + 5, n1 == n0 + 5 ? "OK" : "FAIL");

    /* 3. Try a real-time policy: expected to fail without privileges.
     * That failure is itself the lesson (EPERM). */
    struct sched_param rt = { .sched_priority = 1 };
    if (sched_setscheduler(0, SCHED_FIFO, &rt) != 0)
        printf("sched_setscheduler(FIFO) -> %s (expected without root)\n",
               strerror(errno));
    else
        printf("sched_setscheduler(FIFO) succeeded (running as root?)\n");

    /* 4. CPU affinity: how many CPUs are we allowed on. */
    cpu_set_t set;
    CPU_ZERO(&set);
    if (sched_getaffinity(0, sizeof(set), &set) == 0)
        printf("affinity: %d CPU(s) available\n", CPU_COUNT(&set));
    else
        perror("sched_getaffinity");

    return n1 == n0 + 5 ? 0 : 1;
}
