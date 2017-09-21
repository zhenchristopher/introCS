#include <stdio.h>

int main(int argc, char *argv[]) {
    int i = 10;
    int *j = &i;
    int **k = &j;
    printf("%x\t%d\n", &i, i);
    printf("%x\t%x\t%d\n", &j, j, *j);
    printf("%x\t%x\t%x\t%d\n", &k, k, *k, **k);
    return 0;
}