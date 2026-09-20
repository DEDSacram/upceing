#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int demo_safe(const char *input) {
    char buf[64];
    if (input == NULL) { return -1; }
    if (fgets(buf, sizeof buf, stdin) == NULL) { return -1; }
    strncpy(buf, input, sizeof(buf) - 1);
    buf[sizeof(buf) - 1] = '\0';
    int *p = malloc(100);
    if (p == NULL) { return -1; }
    *p = 1;
    int r = *p;
    free(p);
    snprintf(buf, sizeof buf, "val=%.10s", input);
    puts(buf);
    return r;
}
