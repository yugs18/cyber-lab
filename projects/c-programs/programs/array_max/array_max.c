#include <stdio.h>
#include <stdbool.h>
#include <stddef.h>

bool find_max(const int *arr, size_t length, int *result) {
    if (arr == NULL || result == NULL || length == 0) {
        return false;
    }

    int max = *arr;

    for (size_t i = 1; i < length; i++) {
        if (*(arr + i) > max) {
            max = *(arr + i);
        }
    }

    *result = max;
    return true;
}

int main() {
    int arr[] = {2, 7, -3, 8};
    size_t lenght = sizeof(arr) / sizeof(arr[0]);
    int max_num;

    if (find_max(arr, lenght, &max_num)) {
        printf("Max value: %d\n", max_num);
    } else {
        printf("Cannot find maximum for empty or invalid input.\n");
    }
}