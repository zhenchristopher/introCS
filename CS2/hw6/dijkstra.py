# Christopher Zhen
# February 14, 2017
# dijkstra.py

import math
import numpy as np

# Each element in the heap is an Item.  That Item contains the value (label) associated
# with a vertex as well as the number of that vertex.  The minheap is based on the 
# values, so that the Item with smallest value is a the top of the heap. 
# We also overload the < (lt) and > (gt) operators so that Items can be compared 
# based on their values.
class Item:
    def __init__(self, value, vertex):
        self.value = value
        self.vertex = vertex

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __repr__(self):
        return "<value: " + str(self.value) + " vertex: " + str(self.vertex) + ">"

class PriorityQueueHeap:
    def __init__(self):
        self.length = 4    # initial length of array representing heap      
        self.elements = 0  # number of elements currently in heap    
        self.array = np.empty(self.length, object)
        self.index = np.empty(self.length, np.int)

    def insert(self, item):
        """ insert a new Item into the heap. """
        self.elements += 1
        if self.elements >= self.length:  
            self.extend()
        self.array[self.elements] = item  
        self.index[item.vertex] = self.elements  # set the index in the heap
        currentIndex = self.elements             
        while currentIndex > 1 and self.array[int(currentIndex/2)] > \
                self.array[currentIndex]:
            # swap child and parent
            self.swap(currentIndex, int(currentIndex/2))
            currentIndex = int(currentIndex/2)
        
    def extend(self):
        """ extend the arrays when they fill. """
        newArray = np.empty(self.length*2, object)
        newIndex = np.empty(self.length*2, int)
        for i in range(self.length):
            newArray[i] = self.array[i]
            newIndex[i] = self.index[i]
        self.array=newArray
        self.index = newIndex
        self.length *= 2

    def deleteMin(self):
        """ delete and return the Item with smallest value from the heap. """
        if self.elements == 0: return None
        else:
            output = self.array[1]
            self.swap(1, self.elements)
            self.elements -= 1
            current = 1
            while current < self.elements:
                leftChildIndex = current * 2
                rightChildIndex = current * 2 + 1
                if leftChildIndex > self.elements:
                    break
                elif leftChildIndex <= self.elements and rightChildIndex > self.elements:
                    if self.array[current] > self.array[leftChildIndex]:
                        self.swap(current, leftChildIndex)
                    break
                elif self.array[current] > self.array[leftChildIndex] or \
                     self.array[current] > self.array[rightChildIndex]:
                    if self.array[leftChildIndex] < self.array[rightChildIndex]:
                        self.swap(current, leftChildIndex)
                        current = leftChildIndex
                    else:
                        self.swap(current, rightChildIndex)
                        current = rightChildIndex
                else: 
                    break
            return output

    def decreaseKey(self, vertex, newValue):
        """ Decreases the element at location p to offer value
        and returns the new location of the data in the heap. """
        self.array[self.index[vertex]].value = newValue
        currentIndex = self.index[vertex]          
        while currentIndex > 1 and self.array[int(currentIndex/2)] > \
                self.array[currentIndex]:
            # swap child and parent
            self.swap(currentIndex, int(currentIndex/2))
            currentIndex = int(currentIndex/2)

    def swap(self, index1, index2):
        """ Swap the Items at index1 and index2 in the heap.  
        Since index1 and index2 are the indices of Items in the heap, they each
        correspond to vertices in the heap; call them vertex1 and vertex2.  When
        this swap is performed, we also update self.index so that we can find
        these Items from the self.index table. """
        temp = self.array[index1]
        self.index[temp.vertex] = index2
        self.index[(self.array[index2]).vertex] = index1
        self.array[index1] = self.array[index2]
        self.array[index2] = temp

    def __repr__(self):
        """ Return a string representation of the heap. """
        output = ""
        for i in range(1, self.elements+1):
            item = self.array[i]
            output = output + str(item) + "\n"
        return output
            

INF = float("inf")

test= [ [], 
        [(2, 20), (6, 50)],
        [(1, 20), (3, 70), (6, 30), (5, 10)],
        [(2,70), (5, 40), (4, 90)],
        [(5, 60), (3, 90)],
        [(4, 60), (3, 40), (2, 10), (6, 80)],
        [(5, 80), (1, 50), (2, 30)] ]


def dijkstra(start, map):
    """ Takes a start vertex number, end vertex number, and a map
    in adjacency list form and returns the length of the shortest path
    from start to end. """
    Q = PriorityQueueHeap()
    n = len(map)
    Distance = [None] * n  # Array of distances from start
    # pass <-- Fill in Dijkstra's Algorithm here!
    for i in range(n):
        if i == start:
            Q.insert(Item(0, i))
        else:
            Q.insert(Item(INF, i))
    for i in range(n):
        #loop through all the points
        vertex = Q.deleteMin()
        #pop off the closest point
        Distance[vertex.vertex] = vertex.value
        for neighbor in map[vertex.vertex]:
            #check all the neighbors of that point
            if Q.index[neighbor[0]] <= Q.elements:
                #make sure that we haven't already found the shortest path to
                #that neighbor
                if vertex.value + neighbor[1] < Q.array[Q.index[neighbor[0]]].value:
                    #offer the distance through the vertex to the neighbor
                    Q.decreaseKey(neighbor[0], vertex.value + neighbor[1])
        print(Q)
    return Distance
