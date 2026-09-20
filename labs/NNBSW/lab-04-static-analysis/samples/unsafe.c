#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void demo(char *input) {
    char buf[64];
    gets(buf);                        /* BANNED-GETS */
    strcpy(buf, input);               /* UNBOUNDED-COPY */
    char out[128];
    sprintf(out, "val=%s", input);    /* SPRINTF */
    int *p = malloc(100);             /* UNCHECKED-MALLOC (no NULL check) */
    *p = 1;
    system("ls -la");                 /* SHELL-EXEC */
    printf("%s %d\n", out, *p);
}
