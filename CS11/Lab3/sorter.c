/* Christopher Zhen
 * czhen
 * Code that sorts a sequence of numbers from the command line
 * using either bubble sort or minimum element sort
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

/* max num of items */
#define maxItems 32

int main(int argc, char *argv[]);
void bubbleSort(int sorted_list[], int list_index);
void minSort(int sorted_list[], int list_index);

/* main: returns the sorted list
 * arguments: [-b]: use bubble sort (else use min elem sort),
 * [-q]: quiet, number 1 (number 2 ... number 32)
 * return value: returns sorted list
 */

int main(int argc, char *argv[]) {
    int i;
    /* keep track of how many numbers we need to sort */
    int list_index = 0;
    int bubble = 0;
    int quiet = 0;
    /* initialize the sorted array */
    int sorted_list[maxItems];
    for(i = 1; i < argc; i++) {
        /* check if we need to use bubble sort */
        if(strcmp(argv[i], "-b") == 0) {
            bubble = 1;
        }
        /* check if we need to suppress output */
        else if(strcmp(argv[i], "-q") == 0) {
            quiet = 1;
        }
        else {
            /* error if more than 32 numbers */
            if(list_index >= maxItems) {
                fprintf(stderr, "usage: %s [-b] [-q] number1 [number 2 "
                    "... ] (maximum 32 numbers)", argv[0]);
                exit(1);
            }
            sorted_list[list_index] = atoi(argv[i]);
            list_index++;
        }
    }
    /* error if no numbers */
    if(list_index == 0) {
        fprintf(stderr, "usage: %s [-b] [-q] number1 [number 2 "
            "... ] (maximum 32 numbers)", argv[0]);
        exit(1);
    }
    /* implement bubble sort */
    if(bubble == 1) {
        bubbleSort(sorted_list, list_index);
    }
    /* implement min sort */
    else {
        minSort(sorted_list, list_index);
    }
    /* print if not suppressed */
    if(quiet == 0) {
        for(i = 0; i < list_index; i++) {
            printf("%d\n", sorted_list[i]);
        }
    }
    return 0;
}

/* bubbleSort: implement bubble sort to sort the array
 * arguments: sorted_list: list that requires sorting, list_index: number of 
 * elements that need sorting
 * return value: void, sorts sorted_list
 */

void bubbleSort(int sorted_list[], int list_index) {
    int i, j, temp;
    /* first loop to change which index we sort to (since
     * the last item of each iteration is sorted
     */
    for(i = list_index; i > 1; i--) {
        /* second loop to iterate all the items that need to be sorted */
        for(j = 0; j < i - 1; j++) {
            /* swap elements i and j if they are out of order */
            if(sorted_list[j] > sorted_list[j+1]) {
                temp = sorted_list[j];
                sorted_list[j] = sorted_list[j+1];
                sorted_list[j+1] = temp;
            }
        }
    }
    /* verify list is sorted */
    for(i = 1; i < list_index; i++) {
        assert(sorted_list[i] >= sorted_list[i-1]);
    }
}

/* minSort: impelemnt minimum element sort to sort array
 * arguments: sorted_list: list that requires sorting, list_index:
 * elements that need sorting
 * return value: void, sorts sorted_list
 */

void minSort(int sorted_list[], int list_index) {
    int start, i, temp, smallest;
    /* find minimum element and bump to start, then increment start */
    for(start = 0; start < list_index; start++) {
        smallest = start;
        for(i = start; i < list_index; i++) {
            /* label item smallest if it's the smallest so far */
            if(sorted_list[i] < sorted_list[smallest]) {
                smallest = i;
            }
        }
        /* swap the smallest item and the first unsorted item */
        temp = sorted_list[start];
        sorted_list[start] = sorted_list[smallest];
        sorted_list[smallest] = temp;
    }
    /* verify list is sorted */
    for(i = 1; i < list_index; i++) {
        assert(sorted_list[i] >= sorted_list[i-1]);
    }
}