#include <stdio.h>
#include <stddef.h>

/*
 * print_array:
 * Prints the elements of an integer array by iterating through memory using a pointer.
 *
 * Parameters:
 *   arr    - Pointer to the first element of the array.
 *   length - Number of elements to print.
 *
 * Note:
 *   We use arr + i to move to the next element in memory. Since arr is a pointer to int,
 *   adding i advances by i * sizeof(int) bytes, which correctly reaches the next integer.
 */
void print_array(const int *arr, size_t length) {
    /* Loop through each index from 0 up to length - 1. */
    for (size_t i = 0; i < length; i++) {
        /* Dereference the pointer at the current index and print the integer value. */
        printf("%d", *(arr + i));

        /* Print a comma between values, but not after the last one. */
        if (i + 1 < length) {
            printf(", ");
        }
    }

    /* Move to the next line after printing the entire array. */
    printf("\n");
}

int main() {
    /* Create an integer array with 4 values. */
    const int numbers[] = {10, 20, 30, 40};

    /*
     * Compute array_size as the number of elements in numbers.
     * sizeof(numbers) gives the total number of bytes used by the whole array,
     * and sizeof(numbers[0]) gives the size of one element.
     * Their division yields the count of elements.
     */
    size_t array_size = sizeof(numbers) / sizeof(numbers[0]);

    /* Pass the array and its length to the printing function. */
    print_array(numbers, array_size);

    /* Return 0 to indicate successful program execution. */
    return 0;
}