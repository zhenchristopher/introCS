/* Christopher Zhen
 * czhen
 * code that uses array notation to create and print a user-specified
 * 1D cellular automata
 */

#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include "memcheck.h"

int main(int argc, char *argv[]);
int update(int cellArray[], int cellNum);
int printCell(int cellArray[], int cellNum);

/* main: main file for running and printing the cell automata for a user-
 * defined number of cells and generations
 * arguments: command line arguments where the first is the number of cells
 * and second is the number of generations
 * returns: 0 if successful, prints the generations
 */

int main(int argc, char *argv[]) {
    int i, cellNum, genNum, *cellArray;
    /* print usage statement if we don't have the right number of args */
    if(argc != 3) {
        fprintf(stderr, "usage: %s number of cells number of generations", 
            argv[0]);
        exit(1);
    }
    cellNum = atoi(argv[1]);
    genNum = atoi(argv[2]);
    cellArray = (int *) calloc(cellNum, sizeof(int));
    /* check to see if memory allocation worked */
    if(cellArray == NULL) {
        fprintf(stderr, "Error! Memory allocation failed!\n");
        exit(1);
    }
    srand(time(0));
    /* randomly assign 0 or 1 to all but first and last items */
    for(i = 1; i < (cellNum - 1); i++) {
        cellArray[i] = rand() % 2;
    }
    printCell(cellArray, cellNum);
    /* update cellArray and print after each generation */
    for(i = 0; i < (genNum - 1); i++) {
        update(cellArray, cellNum);
        printCell(cellArray, cellNum);
    }
    free(cellArray);
    print_memory_leaks();
    return 0;
}

/* update: using the rules defined in the lab, update original cell array
 * arguments: cellArray[]: array of current generation, cellNum: number of
 * cells in each generation
 * returns: 0 if successful, modifies the current array for the next 
 * generation
 */

int update(int cellArray[], int cellNum) {
    int i;
    /* initialize another array to temporarily store new generation */
    int *cellArray1 = (int *) calloc(cellNum, sizeof(int));
    if(cellArray1 == NULL) {
        fprintf(stderr, "Error! Memory allocation failed!\n");
        exit(1);
    }
    /* follow rules of generating new cells */
    for(i = 1; i < (cellNum - 1); i++) {
        if(cellArray[i-1] + cellArray[i+1] == 1 && cellArray[i] == 0) {
            cellArray1[i] = 1;
        }
        else {
            cellArray1[i] = 0;
        }
    }
    /* transfer new generation back to original array */
    for(i = 0; i < cellNum; i++) {
        cellArray[i] = cellArray1[i];
    }
    free(cellArray1);
    return 0;
}

/* printCell: prints a graphical representation of cell states for each
 * generation
 * arguments: cellArray[]: array of current generation, cellNum: number of
 * cells in each generation
 * returns: 0 if successful, prints each generation of cells
 */

int printCell(int cellArray[], int cellNum) {
    int i;
    /* print "." for empty and "*" for full */
    for(i = 0; i < cellNum; i++) {
        if(cellArray[i] == 0) {
            printf(".");
        }
        else {
            printf("*");
        }
    }
    printf("\n");
    return 0;
}