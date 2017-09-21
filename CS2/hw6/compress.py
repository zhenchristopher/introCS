# Christopher Zhen
# February 14, 2017
# compress.py

# This file has all the necessary classes and functions to run Huffman 
# compression

import numpy as np

class Item:
    def __init__(self, value, frequency):
        self.value = value
        self.frequency = frequency

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __gt__(self, other):
        return self.frequency > other.frequency

    def __repr__(self):
        return "<value: " + str(self.value) + " frequency: " + str(self.frequency) + ">"

class PriorityQueueHeap:
    def __init__(self):
        self.length = 4    # initial length of array representing heap      
        self.elements = 0  # number of elements currently in heap    
        self.array = np.empty(self.length, object)

    def insert(self, item):
        """ insert a new Item into the heap. """
        self.elements += 1
        if self.elements >= self.length:  
            self.extend()
        self.array[self.elements] = item  
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

    def swap(self, index1, index2):
        """ Swap the Items at index1 and index2 in the heap.  
        Since index1 and index2 are the indices of Items in the heap, they each
        correspond to vertices in the heap; call them frequency1 and frequency2.  When
        this swap is performed, we also update self.index so that we can find
        these Items from the self.index table. """
        temp = self.array[index1]
        self.array[index1] = self.array[index2]
        self.array[index2] = temp

    def __repr__(self):
        """ Return a string representation of the heap. """
        output = ""
        for i in range(1, self.elements+1):
            item = self.array[i]
            output = output + str(item) + "\n"
        return output

class Node:
    '''node class for the binary search tree'''
    def __init__(self, data = None):
        self.data = data
        self.leftChild = None
        self.rightChild = None
        self.parent = None
    
    #return whether the node is a leaf
    def isLeaf(self):
        return self.numChildren() == 0
    
    #return how many children the node has
    def numChildren(self):
        counter = 0
        if self.leftChild != None:
            counter += 1
        if self.rightChild != None:
            counter += 1
        return counter
    
    #return whether the node is the root of a tree
    def isRoot(self):
        return self.parent == None
        
    #return whether the node is a leftChild
    def isLeftChild(self):
        return self.parent.leftChild == self
        
    #return whether the node is a rightChild
    def isRightChild(self):
        return self.parent.rightChild == self
        
class BSTSet:
    '''binary search tree class'''
    def __init__(self):
        self.root = None
        
    #return whether the tree is empty
    def isEmpty(self):
        return self.root == None
        
    #return the string representation of the tree
    def __repr__(self):
        output = ''
        return self.reprHelper(self.root)
    
    #function to help return the string representation of the string
    def reprHelper(self, current):
        if current == None:
            return ''
        else:
            return self.reprHelper(current.leftChild) + ' ' + str(current.data) + ' ' + self.reprHelper(current.rightChild)

def buildTree(frequencies):
    ''' Builds the Huffman tree from a list of values/frequencies which 
    are items where the value is a Node '''
    Q = PriorityQueueHeap()
    for item in frequencies:
        Q.insert(item)
    while Q.elements > 1:
        #remove the two nodes with the lowest frequencies and merge them
        low1 = Q.deleteMin()
        low2 = Q.deleteMin()
        newFreq = low1.frequency + low2.frequency
        newValue = Node(newFreq)
        newValue.leftChild = low1.value
        newValue.rightChild = low2.value
        Q.insert(Item(newValue, newFreq))
    huffTree = BSTSet()
    huffTree.root = (Q.deleteMin()).value
    return huffTree

def huffCode(huffTree, code=''):
    ''' Determine the huffman code given the tree recursively '''
    if huffTree.isLeaf():
        return [str(huffTree.data), code]
    else:
        return huffCode(huffTree.leftChild, code + '0') + huffCode(huffTree.rightChild, code + '1')

def readCode(huffCode):
    ''' Makes a dictionary out of the huffman codes found previously '''
    finalCode = {}
    i = 0
    while i < len(huffCode):
        finalCode[huffCode[i]] = huffCode[i+1]
        i += 2
    return finalCode

def buildCode(frequencies):
    ''' Bundle buildTree, huffCode, and readCode together '''
    return readCode(huffCode(buildTree(frequencies).root))

def computeFrequencies(file):
    ''' Computes the frequencies of letters in a string '''
    n = len(file)
    frequencies = []
    while len(file) != 0:
        symbol = file[0]
        freq = sum([1 for letter in file if letter == symbol])/n
        # remove all matching symbols from string
        file = [letter for letter in file if letter != symbol]
        frequencies += [Item(Node(symbol),freq)]
    return frequencies

def writeHuffmanKey(finalCode, filename, totalbits):
    ''' Saves the huffman key file under the filename'''
    f = open(filename,'w')
    f.write(str(len(finalCode)) + '\n')
    f.write(str(totalbits) + '\n')
    for key, value in finalCode.items():
        f.write(str(key) + str(value) + '\n')
    f.close()

def translateChunk(string, finalCode):
    ''' Takes the file and translates it into bits/bytes based on the
    huffman code'''
    fileBits = ''
    for symbol in string:
        fileBits += finalCode[symbol]
    fileBytes = []
    i = 0
    while i+8 < len(fileBits):
        #iterate through 8 bits at a time
        fileBytes += [int(fileBits[i:i+8],2)]
        i += 8
    lastByte = fileBits[i:]
    fileBytes += [int(lastByte,2)]
    return[fileBits, fileBytes]

def writeHuffman(fileBytes, filename):
    ''' Saves the compressed huffman file as bytes '''
    f = open(filename,'wb')
    f.write(bytes(fileBytes))
    f.close()

def readHuffman(byteFile, charFile):
    ''' Saves the compressed, jumbled huffman file '''
    f = open(byteFile, 'rb')
    readBytes = f.read()
    f.close()
    f1 = open(charFile, 'w')
    f1.write(str(readBytes))
    f1.close()

def main():
    ''' Main file for compression '''
    file = str(input("Enter a file to compress: "))
    f = open(file, 'r')
    text = f.read()
    f.close()
    frequencies = computeFrequencies(text)
    finalCode = buildCode(frequencies)
    [fileBits, fileBytes] = translateChunk(text, finalCode)
    writeHuffmanKey(finalCode, file + '.HUFFMAN.KEY', len(fileBits))
    writeHuffman(fileBytes, file + '.HUFFMAN')
    readHuffman(file + '.HUFFMAN', file + '.JUMBLE')
    print("Original file: " + file + '\n' + "Distinct characters: " + \
        str(len(frequencies)) + '\n' + "Total bytes: " + str(len(text)) + \
        '\n' + "Compressed text length in bytes: " + str(len(fileBytes)) + \
        '\n' + "Asymptotic compression ratio: " + \
        str(len(fileBytes)/len(text)))
    return

if __name__ == '__main__':
    main()
