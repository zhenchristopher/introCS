/* Chris Zhen
 * czhen
 * CS 11, C Track, lab 7
 *
 * FILE: hash_table.c
 *
 *       Implementation of the hash table functionality.
 *
 */

/*
 * Include the declaration of the hash table data structures
 * and the function prototypes.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hash_table.h"
#include "memcheck.h"

/* Number of slots in the hash table array. */
#define NSLOTS 128

/*** Hash function. ***/

/* hash: compute the hash for a key
 * arguments: s: key
 * returns: integer representing hash value
 */
int hash(char *s)
{
    int i = 0;
    int finalHash = 0;
    /* add current letter to hash */
    while(s[i] != 0) {
        finalHash += (int) s[i];
        i++;
    }
    return finalHash % NSLOTS;
}


/*** Linked list utilities. ***/

/* Create a single node. */

/* node: creates a node where next = NULL
 * arguments: key: key for looking up node, value: value stored in node
 * returns: created node
 */
node *create_node(char *key, int value)
{
    /* initialize node */
    node *newNode = (node *)malloc(sizeof(node));
    if(newNode == NULL) {
        fprintf(stderr, "Fatal error: out of memory. "
                "Terminating program.\n");
        exit(1);
    }
    newNode->key = key;
    newNode->value = value;
    newNode->next = NULL;
    return newNode;
}


/* Free all the nodes of a linked list. */

/* free_list: free all nodes in a linked list
 * arguments: list: list to be freed
 * returns: void, frees list
 */
void free_list(node *list) 
{
    node *n;     /* a single node of the list */
    while(list != NULL) {
        n = list;
        list = list->next;
        /*
         * 'n' now points to the first element of the list, while
         * 'list' now points to everything but the first element.
         * Since nothing points to 'n', it can be freed.
         */
        /* free the key as well */
        free(n->key);
        free(n);
    }
}


/*** Hash table utilities. ***/

/* Create a new hash table. */

/* hash_table: creates a new hash table
 * arguments: none
 * returns: newly made hash table 
 */
hash_table *create_hash_table()
{
    int i;
    /* initialize hash table */
    hash_table *newHashTable = malloc(sizeof(hash_table));
    /* initialize slots array of pointers */
    newHashTable->slot = (node **) malloc(NSLOTS * sizeof(node));
    /* set all pointers to point to NULL pointer */
    for(i = 0; i < NSLOTS; i++) {
        *(newHashTable->slot + i) = NULL;
    }
    return newHashTable;
}


/* Free a hash table. */

/* free_hash_table: frees the hash table
 * arguments: ht: hash table to be freed
 * returns: none
 */
void free_hash_table(hash_table *ht)
{
    int i;
    /* iterate through the slots and free each list */
    for(i = 0; i < NSLOTS; i++) {
        free_list(*(ht->slot + i));
    }
    /* free slots and table itself */
    free(ht->slot);
    free(ht);
}


/*
 * Look for a key in the hash table.  Return 0 if not found.
 * If it is found return the associated value.
 */

/* get_value: gets the stored value for the given key
 * arguments: ht: hash table, key: desired key
 * returns: value stored at the key 
 */
int get_value(hash_table *ht, char *key)
{
    int value, found;
    node **address, *current;
    /* initialize value */
    value = 0;
    found = 0;
    /* find address of key */
    address = ht->slot + hash(key);
    current = *address;
    /* search for key in list */
    while(current != NULL && !found) {
        /* if found return the value */
        if(strcmp(current->key, key) == 0) {
            value = current->value;
            found = 1;
        }
        /* else keep looking */
        current = current->next;
    }
    return value;
}


/*
 * Set the value stored at a key.  If the key is not in the table,
 * create a new node and set the value to 'value'.  Note that this
 * function alters the hash table that was passed to it.
 */

/* set_value: sets the value stored at given key. If key isn't in the 
 * table, it creates a new entry at the beginning of the list for that
 * hash value
 * arguements: ht: hash table to be changed, key: key to look for, 
 * value: new value
 * returns: none
 */
void set_value(hash_table *ht, char *key, int value)
{
    int set = 0;
    node *newNode, **address, *current;
    /* initialize address like above */
    address = ht->slot + hash(key);
    current = *address;
    /* add node if nothing there */
    if(*address == NULL) {
        newNode = create_node(key, value);
        *address = newNode;
    }
    /* search through list for key if there's a list */
    else {
        while(current != NULL && !set) {
            /* if key found, just update the value */
            if(strcmp(current->key, key) == 0) {
                current->value = value;
                set = 1;
                /* free key if not put in table */
                free(key);
            }
            current = current->next;
        }
        /* if we didn't find the key make a new one */
        if(!set) {
            newNode = create_node(key, value);
            newNode->next = *address;
            *address = newNode;
        }
    }
}


/* Print out the contents of the hash table as key/value pairs. */

/* print_hash_table: print out the hash table as key/value pairs
 * arguments: ht: hash table
 * returns: none
 */
void print_hash_table(hash_table *ht)
{
    int i;
    node **current = ht->slot;
    node *currNode;
    /* loop through the slots in the ht */
    for(i = 0; i < NSLOTS; i++) {
        currNode = *current;
        /* loop through the list in each slot */
        while(currNode != NULL) {
            printf("%s %d\n", currNode->key, currNode->value);
            currNode = currNode->next;
        }
        current++;
    }
}


