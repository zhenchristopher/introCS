# heaptest.py
# Compares the performance of heap and array implementations of 
# priority queues

import time
import random
import numpy as np

SIZE = 30000  # Run experiment on SIZE numbers

class PriorityQueueHeap:
    def __init__(self):
        self.length = 10      # element 0 is unused!
        self.elements = 0     # elements in the heap so far
        self.array = np.empty(self.length, np.float)  # allocate array

    def insert(self, item):
        """ inserts item into the priority queue """
        #extend the array if we are maxed out
        if self.elements==self.length:
            self.extend()
        self.elements += 1
        self.array[self.elements-1] = item
        index = self.elements - 1
        #bubble item up list
        while item < self.array[int(np.floor((index-1)/2))]:
            self.swap(index,int(np.floor((index-1)/2)))
            index = int(np.floor((index-1)/2))
        
    def extend(self):
        """ Extends self.array by allocating a new array of twice the 
        length and copying the data from the old array to the new array. """
        self.length = self.length*2
        temp = np.empty(self.length, np.float)
        temp[:int(self.length/2)] = self.array
        self.array = temp

    def deleteMin(self):
        """ removes minimum item from the priority queue and returns it.
        returns None if the priority queue is empty."""
        if self.elements > 0:
            item = self.array[0]
            self.swap(0,self.elements-1)
            self.elements += -1
            index = 0
            #initialize all variables
            left = right = leftless = False
            first = True
            #bubble item down list
            while (left or right) or first:
                first = False
                #swap with left child if it's smaller than parent and right
                if left and leftless:
                    self.swap(index,2*index+1)
                    index = 2*index+1
                #otherwise swap with right if it's smallest
                elif right:
                    self.swap(index,2*index+2)
                    index = 2*index+2
                left = right = False
                leftless = True
                #if we have a left leaf, see if it's smaller
                if 2*index+1 < self.elements:
                    left = self.array[index] > self.array[2*index+1]
                #if we have a right leaf, see if it's smaller
                if 2*index+2 < self.elements:
                    right = self.array[index] > self.array[2*index+2]
                    leftless = self.array[2*index+1] < self.array[2*index+2]
            return item
        else:
            return None

    def swap(self, i, j):
        """ swaps elements i and j in the array """
        temp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = temp

class PriorityQueueList:
    def __init__(self):
        self.contents = []

    def insert(self, item):
        """ inserts item into the priority queue """
        self.contents.append(item)
        
    def deleteMin(self):
        """ removes minimum item from the priority queue and returns it. 
        returns None if the priority queue is empty. """
        if self.contents == []: return None
        else:
            smallestItem = min(self.contents)
            self.contents.remove(smallestItem)
            return smallestItem

def main():
    # make two priority queues using the two different implementations
    priorityQueues = [PriorityQueueHeap(), \
                      PriorityQueueList()]
    
    # make a random permutation of the numbers from 1 to SIZE
    nums = list(range(SIZE))
    random.shuffle(nums)

    for PQ in priorityQueues:
        startTime = time.time()
        # Insert all of the numbers into the priority queue
        for num in nums:
            PQ.insert(num)
        # Delete the numbers from the priority queue by successive
        # deleteMin() operations
        for i in range(SIZE):
            PQ.deleteMin()
        endTime = time.time()
        elapsedTime = endTime-startTime
        print(str(PQ) + ": " + str(elapsedTime) + " seconds")

main()
