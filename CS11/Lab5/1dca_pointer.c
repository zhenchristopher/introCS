/* Christopher Zhen
 * czhen
 * code that uses pointer notation to create and print a user-specified
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
    int i, *cell, cellNum, genNum, *cellArray;
    if(argc != 3) {
        fprintf(stderr, "usage: %s number of cells number of generations", 
            argv[0]);
        exit(1);
    }
    cellNum = atoi(*(argv + 1));
    genNum = atoi(*(argv + 2));
    /* print usage statement if we don't have the right number of args */
    cellArray = (int *) calloc(cellNum, sizeof(int));
    /* check to see if memory allocation worked */
    if(cellArray == NULL) {
        fprintf(stderr, "Error! Memory allocation failed!\n");
        exit(1);
    }
    srand(time(0));
    /* assign index of cellArray to new variable */
    cell = cellArray + 1;
    /* randomly assign 0 or 1 to all but first and last items */
    for(i = 1; i < (cellNum - 1); i++) {
        *cell = rand() % 2;
        cell++;
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
    int i, *cellL, *cell, *cellR, *cell1;
    /* initialize another array to temporarily store new generation */
    int *cellArray1 = (int *) calloc(cellNum, sizeof(int));
    if(cellArray1 == NULL) {
        fprintf(stderr, "Error! Memory allocation failed!\n");
        exit(1);
    }
    /* assign i - 1 to cellL, i to cell, and i + 1 to cellR */
    cellL = cellArray; 
    cell = cellArray + 1; 
    cellR = cellArray + 2;
    /* assign cellArray1 to cell1 */
    cell1 = cellArray1 + 1; 
    /* follow rules of generating new cells */
    for(i = 1; i < (cellNum - 1); i++) {
        if((*cellL + *cellR) == 1 && *cell == 0) {
            *cell1 = 1;
            /* increment all */
            cellL++; cell++; cellR++; cell1++;
        }
        else {
            *cell1 = 0;
            cellL++; cell++; cellR++; cell1++;
        }
    }
    /* re-intialize cell and cell1 */
    cell = cellArray; 
    cell1 = cellArray1;
    /* transfer new generation back to original array */
    for(i = 0; i < cellNum; i++) {
        *cell = *cell1;
        cell++; cell1++;
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
    int i, *cell;
    cell = cellArray;
    /* print "." for empty and "*" for full */
    for(i = 0; i < cellNum; i++) {
        if(*cell == 0) {
            printf(".");
            cell++;
        }
        else {
            printf("*");
            cell++;
        }
    }
    printf("\n");
    return 0;
}