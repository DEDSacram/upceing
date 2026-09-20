#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>

#define NPHIL 5

static pthread_mutex_t fork_mx[NPHIL];
/* Release all philosophers at once so every one holds its left fork
 * before anyone reaches for the right fork => deterministic deadlock. */
static pthread_barrier_t ready_b, done_b;

static void msleep(long ms) {
    struct timespec ts = { .tv_sec = ms / 1000,
                           .tv_nsec = (ms % 1000) * 1000 * 1000 };
    nanosleep(&ts, NULL);
}

/* --- Phase 1: naive take-left-then-right, deadlock DEMONSTRATED safely.
 * All philosophers lock their left fork, rendezvous at a barrier (so every
 * left fork is definitely held), then trylock() the right fork exactly once.
 * trylock() never blocks, so every attempt deterministically fails: the
 * system is in the deadly embrace (circular wait). A second barrier keeps
 * everyone holding their fork while all attempts happen, then all release.
 * NOTE: a real blocking lock() here would hang forever -- that is why we
 * use the non-blocking trylock to *detect* the embrace instead. */
static void *naive(void *arg) {
    long id = (long)arg;
    int left = (int)id, right = (int)((id + 1) % NPHIL);
    pthread_mutex_lock(&fork_mx[left]);
    pthread_barrier_wait(&ready_b); /* all hold left now -> circular wait */
    int rc = pthread_mutex_trylock(&fork_mx[right]);
    int ate = (rc == 0);
    if (ate) {
        printf("[naive %ld] ate (no deadlock this time)\n", id);
        pthread_mutex_unlock(&fork_mx[right]);
    }
    pthread_barrier_wait(&done_b); /* nobody releases early */
    pthread_mutex_unlock(&fork_mx[left]);
    return (void *)(long)!ate; /* 1 = starved */
}

/* --- Phase 2: resource ordering fix.
 * Philosopher NPHIL-1 picks forks in reverse order, breaking the
 * circular-wait condition (one of Coffman's 4 conditions). */
static void *ordered(void *arg) {
    long id = (long)arg;
    int first = (int)id, second = (int)((id + 1) % NPHIL);
    if (id == NPHIL - 1) { int t = first; first = second; second = t; }
    pthread_mutex_lock(&fork_mx[first]);
    msleep(10); /* widen the race window: fix must still hold */
    pthread_mutex_lock(&fork_mx[second]);
    printf("[ordered %ld] ate (forks %d,%d)\n", id, first, second);
    pthread_mutex_unlock(&fork_mx[second]);
    pthread_mutex_unlock(&fork_mx[first]);
    return (void *)0;
}

static int run_all(void *(*fn)(void *)) {
    pthread_t th[NPHIL];
    for (long i = 0; i < NPHIL; i++)
        pthread_create(&th[i], NULL, fn, (void *)i);
    int starved = 0;
    for (int i = 0; i < NPHIL; i++) {
        void *ret = NULL;
        pthread_join(th[i], &ret);
        starved += (int)(long)ret;
    }
    return starved;
}

int main(void) {
    for (int i = 0; i < NPHIL; i++)
        pthread_mutex_init(&fork_mx[i], NULL);
    pthread_barrier_init(&ready_b, NULL, NPHIL);
    pthread_barrier_init(&done_b, NULL, NPHIL);

    int starved = run_all(naive);
    printf("naive: %d/%d philosophers starved -> %s\n", starved, NPHIL,
           starved == NPHIL ? "DEADLOCK DEMONSTRATED" : "no full deadlock");
    int ok_deadlock = (starved == NPHIL);

    int leftover = run_all(ordered);
    printf("ordered: %d/%d starved -> %s\n", leftover, NPHIL,
           leftover == 0 ? "FIX WORKS (all ate)" : "FIX FAILED");

    for (int i = 0; i < NPHIL; i++)
        pthread_mutex_destroy(&fork_mx[i]);
    pthread_barrier_destroy(&ready_b);
    pthread_barrier_destroy(&done_b);
    return (ok_deadlock && leftover == 0) ? 0 : 1;
}
