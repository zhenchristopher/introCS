/* Christopher Zhen
 * czhen
 * Function to solve the triangle game using a user defined board
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "triangle_routines.h"

/* number of possible moves */
#define NMOVES 36
/* size of allowable board */
#define BSIZE 15
/* size of allowable move */
#define MSIZE 3

int moves[NMOVES][MSIZE] = {
    {0, 1, 3}, 
    {1, 3, 6}, 
    {3, 6, 10}, 
    {0, 2, 5}, 
    {2, 5, 9}, 
    {5, 9, 14}, 
    {3, 4, 5}, 
    {6, 7, 8}, 
    {7, 8, 9}, 
    {10, 11, 12}, 
    {11, 12, 13}, 
    {12, 13, 14}, 
    {1, 4, 8}, 
    {4, 8, 13}, 
    {3, 7, 12}, 
    {2, 4, 7}, 
    {4, 7, 11}, 
    {5, 8, 12}, 
    {3, 1, 0}, 
    {6, 3, 1}, 
    {10, 6, 3}, 
    {5, 2, 0}, 
    {9, 5, 2}, 
    {14, 9, 5}, 
    {5, 4, 3}, 
    {8, 7, 6}, 
    {9, 8, 7}, 
    {12, 11, 10}, 
    {13, 12, 11}, 
    {14, 13, 12}, 
    {8, 4, 1}, 
    {13, 8, 4}, 
    {12, 7, 3}, 
    {7, 4, 2}, 
    {11, 7, 4}, 
    {12, 8, 5} 
};

/* Return the number of pegs on the board. */
int npegs(int board[]);

/* Return 1 if the move is valid on this board, otherwise return 0. */
int valid_move(int board[], int move[]);

/* Make this move on this board. */
int make_move(int board[], int move[]);

/* Unmake this move on this board. */
void unmake_move(int board[], int move[]);

/* Solve the game starting from this board.  Return 1 if the game can
 * be solved; otherwise return 0.  Do not permanently alter the board passed
 * in. Once a solution is found, print the boards making up the solution in
 * reverse order
 */
int solve(int board[]);

/* main: function that has the user input a board and attempts to solve it
 * arguments: command line arguments that don't affect program
 * return value: 0, prints solved board or "unsolvable"
 */
int main(int argc, char *argv[]) {
    int board[BSIZE], solvable;
    triangle_input(board);
    solvable = solve(board);
    if(!solvable) {
        printf("Unsolvable");
    }
    return 0;
}

/* npegs: return the number of pegs on the board
 * arguments: board[]: current board
 * return value: number of pegs on the board
 */
int npegs(int board[]) {
    int i;
    /* keep track of the number of pegs */
    int numPegs = 0;
    for(i = 0; i < BSIZE; i++) {
        /* increment if we find a peg */
        if(board[i] == 1) {
            numPegs += 1;
        }
    }
    return numPegs;
}

/* valid_move: returns 1 if move is valid, otherwise 0
 * arguments: board[]: current board, move[]: prospective move
 * return value: 1 or 0 depending on the validity of the move
 */
int valid_move(int board[], int move[]) {
    /* find whether there is a peg in the start, jump and end positions */
    int start = board[move[0]];
    int jump = board[move[1]];
    int end = board[move[2]];
    /* need peg, empty, peg */
    return start == 1 && jump == 1 && end == 0;
}

/* make_move: changes the board according to the move
 * arguments: board[]: current board, move[]: prospective move
 * return value: 1 if move was made, 0 otherwise
 */
int make_move(int board[], int move[]) {
    int i;
    /* check if move is valid */
    if(valid_move(board, move) == 1) {
        /* make move by flipping the pieces */
        for(i = 0; i < MSIZE; i++) {
            board[move[i]] = !board[move[i]];
        }
        /* let us know that we made a move (so we can unmake) */
        return 1;
    }
    return 0;
}

/* unmake_move: undoes changes to the board from a particular move
 * arguments: board[]: current board, move[]: prospective move
 * return value: void
 */
void unmake_move(int board[], int move[]) {
    int i;
    /* make unmove by flipping pieces again */
    for(i = 0; i < MSIZE; i++) {
        board[move[i]] = !board[move[i]];
    }
}

/* solve: recursively find a solution to the current board
 * arguments: board[]: current board
 * return value: prints boards and returns 1 if there is a solution, 
 * otherwise, returns 0
 */
int solve(int board[]) {
    int i, moved;
    /* base case */
    if(npegs(board) == 1) {
        triangle_print(board);
        return 1;
    }
    else {
        for(i = 0; i < NMOVES; i++) {
            /* check if we actually made the move */
            moved = make_move(board, moves[i]);
            if(moved) {
                /* if we made a move check if resulting board is solvable */
                if(solve(board) == 1) {
                    /* unmake and print board */
                    unmake_move(board, moves[i]);
                    triangle_print(board);
                    return 1;
                }
                /* unmake board if not solvable */
                unmake_move(board, moves[i]);
            }
        }
        /* not solvable */
        return 0;
    }
}