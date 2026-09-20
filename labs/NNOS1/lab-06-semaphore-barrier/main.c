#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>

#define NITEMS 10
#define BUFSZ 4
#define NWORKERS 3

/* --- Part 1: producer-consumer with counting semaphores + mutex --- */
static int buf[BUFSZ], in = 0, out = 0;
static sem_t sem_empty, sem_full;
static pthread_mutex_t mx = PTHREAD_MUTEX_INITIALIZER;
static int consumed[NITEMS], nconsumed = 0;

static void *producer(void *arg) {
    (void)arg;
    for (int i = 0; i < NITEMS; i++) {
        sem_wait(&sem_empty);
        pthread_mutex_lock(&mx);
        buf[in] = i;
        in = (in + 1) % BUFSZ;
        pthread_mutex_unlock(&mx);
        sem_post(&sem_full);
    }
    return NULL;
}

static void *consumer(void *arg) {
    (void)arg;
    for (int i = 0; i < NITEMS; i++) {
        sem_wait(&sem_full);
        pthread_mutex_lock(&mx);
        int v = buf[out];
        out = (out + 1) % BUFSZ;
        consumed[nconsumed++] = v;
        pthread_mutex_unlock(&mx);
        sem_post(&sem_empty);
    }
    return NULL;
}

/* --- Part 2: pthread_barrier rendezvous --- */
static pthread_barrier_t barrier;

static void *worker(void *arg) {
    long id = (long)arg;
    printf("[worker %ld] phase 1 done, waiting at barrier...\n", id);
    pthread_barrier_wait(&barrier); /* all meet here */
    printf("[worker %ld] passed barrier, phase 2 done.\n", id);
    return NULL;
}

int main(void) {
    sem_init(&sem_empty, 0, BUFSZ);
    sem_init(&sem_full, 0, 0);
    pthread_t p, c;
    pthread_create(&p, NULL, producer, NULL);
    pthread_create(&c, NULL, consumer, NULL);
    pthread_join(p, NULL);
    pthread_join(c, NULL);

    int ok = (nconsumed == NITEMS);
    for (int i = 0; i < NITEMS && ok; i++)
        if (consumed[i] != i) ok = 0;
    printf("producer-consumer: %d items in order 0..%d -> %s\n",
           nconsumed, NITEMS - 1, ok ? "OK" : "FAIL");
    sem_destroy(&sem_empty);
    sem_destroy(&sem_full);
    if (!ok) return 1;

    pthread_barrier_init(&barrier, NULL, NWORKERS);
    pthread_t w[NWORKERS];
    for (long i = 0; i < NWORKERS; i++)
        pthread_create(&w[i], NULL, worker, (void *)i);
    for (int i = 0; i < NWORKERS; i++)
        pthread_join(w[i], NULL);
    pthread_barrier_destroy(&barrier);
    printf("barrier: all %d workers rendezvoused -> OK\n", NWORKERS);
    return 0;
}
