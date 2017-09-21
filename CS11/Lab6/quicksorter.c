/* Christopher Zhen
 * czhen
 * Code that sorts a sequence of numbers from the command line
 * using quicksort
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "linked_list.h"
#include "memcheck.h"

int main(int argc, char *argv[]);
node* quickSort(node *list);

/* main: function that uses the quicksort algorithm to sort a sequence of
 * numbers from the command line
 * arguments: [-q]: suppress output, numbers from command line
 * returns: sorted list
 */

int main(int argc, char *argv[]) {
    int i;
    /* keep track of how many numbers we need to sort */
    int quiet = 0;
    /* initialize the sorted linked list */
    node *sorted_list, *list;
    sorted_list = NULL;
    for(i = 1; i < argc; i++) {
        /* check if we need to suppress output */
        if(strcmp(argv[i], "-q") == 0) {
            quiet = 1;
        }
        /* add new node to the list */
        else {
            sorted_list = create_node(atoi(argv[i]), sorted_list);
        }
    }
    /* error if no numbers */
    if(sorted_list == NULL) {
        fprintf(stderr, "usage: %s [-q] number1 [number 2 "
            "... ]", argv[0]);
        exit(1);
    }
    /* quicksort our list */
    list = quickSort(sorted_list);
    free_list(sorted_list);
    sorted_list = list;
    /* print if not suppressed */
    if(!quiet) {
        print_list(sorted_list);
    }
    free_list(sorted_list);
    print_memory_leaks();
    return 0;
}

/* quickSort: use quicksort algorithm to recursively sort a list
 * arguments: list: list to be sorted
 * returns: copy of sorted list
 */

node* quickSort(node *list) {
    /* initialize all variables */
    node *first, *smaller, *larger, *tempS, *tempL, *final, *final2, *item;
    /* base case */
    if(list == NULL || list->next == NULL) {
        return copy_list(list);
    }
    first = smaller = larger = NULL;
    /* create a copy of the first item */
    first = create_node(list->data, first);
    /* step through list and add item to smaller or larger */
    for(item = list->next; item != NULL; item = item->next) {
        if(item->data >= first->data) {
            larger = create_node(item->data, larger);
        }
        else {
            smaller = create_node(item->data, smaller);
        }
    }
    /* recursive calls on the smaller and larger lists */
    tempS = quickSort(smaller);
    free_list(smaller);
    smaller = tempS;
    tempL = quickSort(larger);
    free_list(larger);
    larger = tempL;
    /* append the smaller, first, and larger lists */
    final = append_lists(smaller, first);
    final2 = append_lists(final, larger);
    /* free all data */
    free_list(smaller);
    free_list(larger);
    free_list(final);
    free_list(first);
    /* make sure lists are sorted */
    assert(is_sorted(final2));
    return final2;
}