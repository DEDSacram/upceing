#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>
#include <string.h>

#define NTHREADS 4
#define INPUTS 4

static const char *inputs[INPUTS] = {
    "alpha,beta,gamma",
    "one;two;three",
    "red green blue",
    "1:2:3:4",
};
static const char *delims[INPUTS] = { ",", ";", " ", ":" };

/* PITFALL DEMO (kept single-threaded => deterministic):
 * strtok() keeps internal state, so interleaved tokenisation of two
 * strings corrupts both. strtok_r() keeps state in caller memory
 * and is reentrant/thread-safe. */
static void strtok_pitfall_demo(void) {
    char a[] = "alpha,beta,gamma";
    char b[] = "one,two,three";
    char *s1, *s2;

    printf("--- pitfall: strtok() shares hidden state ---\n");
    /* Interleaved tokenisation of two strings with strtok(): */
    strcpy(a, "alpha,beta,gamma");
    strcpy(b, "one,two,three");
    char *t1 = strtok(a, ",");   /* alpha, state -> a */
    char *t2 = strtok(b, ",");   /* one,   state -> b (a's state LOST) */
    char *t3 = strtok(NULL, ",");/* two (continues b, NOT a!) */
    printf("interleaved: t1=%s t2=%s t3=%s  (wanted alpha/one/beta, got alpha/one/two)\n",
           t1, t2, t3);
    (void)s1; (void)s2;

    printf("--- fix: strtok_r() with per-thread state ---\n");
    strcpy(a, "alpha,beta,gamma");
    strcpy(b, "one,two,three");
    char *sa = NULL, *sb = NULL;
    t1 = strtok_r(a, ",", &sa);
    t2 = strtok_r(b, ",", &sb);
    t3 = strtok_r(NULL, ",", &sa); /* correctly continues a */
    printf("interleaved: t1=%s t2=%s t3=%s  (correct)\n", t1, t2, t3);
}

/* THREAD DEMO: each thread tokenises its own string with strtok_r
 * (reentrant => safe) and reports its token count. */
static void *worker(void *arg) {
    long id = (long)arg;
    char buf[64];
    snprintf(buf, sizeof(buf), "%s", inputs[id]);
    int n = 0;
    char *save = NULL, *tok = strtok_r(buf, delims[id], &save);
    while (tok) { n++; tok = strtok_r(NULL, delims[id], &save); }
    printf("[thread %ld] \"%s\" -> %d tokens\n", id, inputs[id], n);
    return (void *)(long)n;
}

int main(void) {
    strtok_pitfall_demo();
    printf("--- threads: %d threads x strtok_r ---\n", NTHREADS);
    pthread_t th[NTHREADS];
    for (long i = 0; i < NTHREADS; i++)
        pthread_create(&th[i], NULL, worker, (void *)i);
    int total = 0;
    for (int i = 0; i < NTHREADS; i++) {
        void *ret = NULL;
        pthread_join(th[i], &ret);
        total += (int)(long)ret;
    }
    printf("total tokens=%d (expected 3+3+3+4=13): %s\n",
           total, total == 13 ? "OK" : "FAIL");
    return total == 13 ? 0 : 1;
}
