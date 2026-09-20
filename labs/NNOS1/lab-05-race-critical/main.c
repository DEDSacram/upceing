#include <pthread.h>
#include <stdio.h>

#define NTHREADS 4
#define INCR 200000

static long counter = 0;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

static void *racy(void *arg) {
    (void)arg;
    for (int i = 0; i < INCR; i++)
        counter++; /* read-modify-write: NOT atomic */
    return NULL;
}

static void *safe(void *arg) {
    (void)arg;
    for (int i = 0; i < INCR; i++) {
        pthread_mutex_lock(&lock);
        counter++;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

static long run(void *(*fn)(void *)) {
    pthread_t th[NTHREADS];
    counter = 0;
    for (int i = 0; i < NTHREADS; i++)
        pthread_create(&th[i], NULL, fn, NULL);
    for (int i = 0; i < NTHREADS; i++)
        pthread_join(th[i], NULL);
    return counter;
}

int main(void) {
    const long expected = (long)NTHREADS * INCR;

    /* Phase 1: race. Result is typically < expected (lost updates).
     * Exact value varies run to run -- that nondeterminism IS the bug. */
    long got_racy = run(racy);
    printf("racy:   got %ld, expected %ld -> %s\n", got_racy, expected,
           got_racy == expected ? "(lucky, still buggy!)" : "LOST UPDATES (race)");

    /* Phase 2: critical section protected by a mutex. Always exact. */
    long got_safe = run(safe);
    printf("mutex:  got %ld, expected %ld -> %s\n", got_safe, expected,
           got_safe == expected ? "OK" : "FAIL");

    return got_safe == expected ? 0 : 1;
}
