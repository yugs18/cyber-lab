#include <stdio.h>

int main(void) {
    int a = 10;
    char b = 'A';
    int c = 20;

    printf("a = %d\n", a);
    printf("b = %c\n", b);
    printf("c = %d\n", c);

    printf("&a = %p\n", (void *)&a);
    printf("&b = %p\n", (void *)&b);
    printf("&c = %p\n", (void *)&c);

    printf("sizeof(a) = %zu\n", sizeof(a));
    printf("sizeof(b) = %zu\n", sizeof(b));
    printf("sizeof(c) = %zu\n", sizeof(c));

    int *p = &a;

    printf("p = %p\n", (void *)p);
    printf("*p = %d\n", *p);

    return 0;
}