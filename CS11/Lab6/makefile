# 
# Makefile for Assignment 6
# Christopher Zhen
# 

CC     = gcc
CFLAGS = -g -Wall -Wstrict-prototypes -ansi -pedantic

quicksorter: quicksorter.o memcheck.o linked_list.o
	$(CC) quicksorter.o memcheck.o linked_list.o -o quicksorter

quicksorter.o: quicksorter.c
	$(CC) $(CFLAGS) -c quicksorter.c

linked_list.o: linked_list.c
	$(CC) $(CFLAGS) -c linked_list.c

memcheck.o: memcheck.c
	$(CC) $(CFLAGS) -c memcheck.c

clean:
	rm -f *.o quicksorter