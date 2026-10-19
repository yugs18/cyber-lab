// Counts how many elements equal to a target value

#include <stdio.h>
#include <stddef.h>


int count_target(int *arr, size_t length, int target) {
    int c = 0;
    for (size_t i = 0; i < length; i++) {
        if (target == *(arr + i)) {
            c++;
        }
    }

    return c;
}


int main() {
    int arr[] = {4, 7, 4, 2, 4};
    size_t length = sizeof(arr) / sizeof(arr[0]);
    int target = 4;

    int count = count_target(arr, length, target);
    printf("Count: %d\n", count);

    return 0;
}