# Christopher Zhen
# February 28, 2017
# tsp.py

# This file has all the necessary classes and functions to run the 
# traveling salesman problem using both the 2-approximation and the
# pairwise-exchange heuristic

import math
import matplotlib.pyplot as plt
import numpy as np

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

class Node:    
    def __init__(self, data = None):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None  # The top of the stack is currently empty
 
    # add a new Node with the given data to the top of the stack
    def push(self, data):
        newNode = Node(data)
        if self.isEmpty():
            self.head = newNode
        else:
            newNode.next = self.head
            self.head = newNode

    # remove the Node at the top of the stack and return its data
    def pop(self):
        output = self.head.data
        if self.head.next == None:
            self.head = None
        else:
            self.head = self.head.next
        return output

    # another name for push; nothing for you to write here!
    def add(self, data):
        self.push(data)

    # another name for pop; nothing for you to write here!
    def remove(self):
        return self.pop()

    # return True if the stack is empty and false otherwise
    def isEmpty(self):
        return self.head == None

    # return a nice string representation of the contents of the stack
    def __repr__(self):
        output = "Stack<"
        for item in self:
            output += str(item) + ","
        if len(output) > 6:
            return output[:len(output)-1] + ">"
        else:
            return output + ">"
            
    def __iter__(self):
        currentNode = self.head
        while currentNode is not None:
            yield currentNode.data
            currentNode = currentNode.next

# Prim's algorithm implementation

INF = float("inf")

test= [ [(1, 10), (2, 100)],
        [(2, 20), (6, 50)],
        [(1, 20), (3, 70), (6, 30), (5, 10)],
        [(2,70), (5, 40), (4, 90)],
        [(5, 60), (3, 90)],
        [(4, 60), (3, 40), (2, 10), (6, 80)],
        [(5, 80), (1, 50), (2, 30)]]

def prims(map):
    ''' Takes an undirected graph in adjacency list form and returns the 
    minimum spanning tree. '''
    Q = PriorityQueueHeap()
    n = len(map)
    MST = [[]] * n  # Array of MST
    for i in range(n):
        if i == 0:
            Q.insert(Item(0, i, None))
        else:
            Q.insert(Item(INF, i, None))
    for i in range(n):
        #loop through all the points
        vertex = Q.deleteMin()
        #pop off the closest point
        if i != 0:
            # add the point to MST[predecessor] as long as it's not the first
            # point
            MST[vertex.predecessor] = MST[vertex.predecessor] + \
                [vertex.vertex]
        for neighbor in map[vertex.vertex]:
            # check all the neighbors of that point
            if Q.index[neighbor[0]] <= Q.elements:
                # make sure that we haven't already added that point to MST
                if neighbor[1] < Q.array[Q.index[neighbor[0]]].value:
                    # offer the distance from the vertex to the neighbor
                    Q.decreaseKey(neighbor[0], neighbor[1],vertex.vertex)
    return MST

def readGraph(filename):
    ''' Read the file into a list '''
    points = []
    f = open(filename,'r')
    first = True
    for line in f:
        # format each line as a tuple (x-coord, y-coord)
        if first:
            points += [int(line)]
            first = False
        else:
            split = line.index(' ')
            points += [(float(line[:split]), float(line[split+1:len(line)-1]))]
    f.close()
    return points

def graphList(points):
    ''' Turn the list of points into an adjacency list '''
    adjList = [[]] * int(points[0])
    for point in range(1,len(points)):
        for neighbor in range(1, len(points)):
            if point != neighbor:
                adjList[point-1] = adjList[point-1] + [(neighbor-1, \
                    distance(points[point],points[neighbor]))]
    return adjList

def distance(a,b):
    ''' Calcualtes the Euclidean distance between points a and b '''
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def genWalk(MST):
    ''' Use DFS to find a preorder traversal of the MST found using Prim's '''
    S = Stack()
    S.push(0)
    visited = []
    while not S.isEmpty():
        point = S.pop()
        for child in reversed(MST[point]):
            if child in visited:
                continue
            else:
                S.push(child)
        visited += [point]
    return visited + [0]

def plot(filename, points, walk):
    ''' Plot the walk found using the approximation '''
    xList = []
    yList = []
    for step in walk:
        xList += [points[step+1][0]]
        yList += [points[step+1][1]]
    plt.plot(xList, yList, 'go-')
    plt.savefig(filename)

def totalDist(points, walk):
    ''' Calculate the distance of the walk found using the approximation '''
    totDist = 0.0
    currentPoint = points[walk[0]+1]
    for step in walk:
        if step == walk[0]:
            continue
        else:    
            nextPoint = points[step+1]
            totDist += distance(currentPoint, nextPoint)
            currentPoint = nextPoint
    return (totDist + distance(currentPoint, points[walk[0]+1]))

def exchange(walk, i, j):
    ''' Perform pairwise exchange on a walk between points i and j '''
    return list(walk[:i]) + list(reversed(walk[i:j+1])) + list(walk[j+1:])

def approx(filename):
    ''' Main file for running the 2-approximation algorithm '''
    points = readGraph(filename)
    adjList = graphList(points)
    walk = genWalk(prims(adjList))
    plot(filename + '.approx.png', points, walk)
    return totalDist(points, walk)

def TSP(filename):
    ''' Main file for running the pairwise exchange heuristic on the 
    2-approximation solution '''
    points = readGraph(filename)
    adjList = graphList(points)
    bestWalk = genWalk(prims(adjList))
    bestCost = totalDist(points, bestWalk)
    testCost = 0
    first = True
    while testCost < bestCost:
        # repeat until we converge
        if first:
            first = False
        else:
            bestCost = testCost
        found = False
        # break if we find a better solution
        for i in range(1,len(bestWalk)-1):
            if found:
                break
            else:
                for j in range(i+1, len(bestWalk)-1):
                    testWalk = exchange(bestWalk, i, j)
                    testCost = totalDist(points, testWalk)
                    if testCost < bestCost:
                        # found a better solution
                        bestWalk = testWalk
                        found = True
                        break
    plot(filename+'.tsp.png', points, bestWalk)
    return bestCost