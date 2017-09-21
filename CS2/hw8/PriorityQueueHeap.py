# Priority Queue implemented using a binary minheap data structure

import numpy as np

# Each element in the heap is an Item.  That Item contains the value (label) associated
# with a vertex as well as the number of that vertex.  The minheap is based on the 
# values, so that the Item with smallest value is a the top of the heap. 
# We also overload the < (lt) and > (gt) operators so that Items can be compared 
# based on their values.
class Item:
    def __init__(self, value, vertex, predecessor):
        self.value = value
        self.vertex = vertex
        self.predecessor = predecessor  # Which vertex gave this value

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

    def decreaseKey(self, vertex, newValue, predecessor):
        """ Decreases the element at location p to offer value
        and returns the new location of the data in the heap. """
        index = self.index[vertex]  # get location of item
        if self.array[index].value < newValue: return
        else:
            self.array[index].value = newValue
            self.array[index].predecessor = predecessor
            current = index
            parent = int(index/2)
            while parent >= 1 and self.array[current] < self.array[parent]:
                self.swap(current, parent)
                current = parent
                parent = int(current/2)
        return 

    def swap(self, index1, index2):
        """ Swap the Items at index1 and index2 in the heap.  
        Since index1 and index2 are the indices of Items in the heap, they each
        correspond to vertices in the heap; call them vertex1 and vertex2.  When
        this swap is performed, we also update self.index so that we can find
        these Items from the self.index table. """
        item1 = self.array[index1]
        item2 = self.array[index2]
        vertex1 = item1.vertex
        vertex2 = item2.vertex

        self.array[index2] = item1
        self.array[index1] = item2
        self.index[vertex1] = index2
        self.index[vertex2] = index1

    def __repr__(self):
        """ Return a string representation of the heap. """
        output = ""
        for i in range(1, self.elements+1):
            item = self.array[i]
            output = output + str(item) + "\n"
        return output
            
