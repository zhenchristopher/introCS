#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void)
{
    int a, i;
    char s[100];
    srand(time(0));
    a = rand()%10 + 1;
    printf("Enter your name: ");
    scanf("%99s", s);
    for(i = 0; i < a; i++)
    {
        if (a % 2 == 0)
        {
            printf("%d: hello, %s!\n", a, s);
        }
        else
        {
            printf("%d: hi there, %s!\n", a, s);
        }
    }
    return 0;
}