# Christopher Zhen
# February 7, 2017
# Deque.py

# This file has the Node and Deque classes

# Fill in the code for all of the methods
# You may add other helper methods as well if you wish.

class Node:
    def __init__(self, data = None):
        self.data = data
        self.next = None
        self.previous = None

class Deque:
    def __init__(self):
        self.head = None
        self.tail = None        

    def addHead(self, data):
        """ Add a new node to the head of the Deque. """
        newNode = Node(data)
        if self.isEmpty():
            self.head = newNode
            self.tail = newNode
        else:
            newNode.next = self.head
            self.head.previous = newNode
            self.head = newNode

    def addTail(self, data):
        """ Add a new node to the tail of the Deque. """
        newNode = Node(data)
        if self.isEmpty():
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.next = newNode
            newNode.previous = self.tail
            self.tail = newNode

    def peekHead(self):
        """ Return the data at the head of the Deque, but don't remove it."""
        return self.head.data

    def removeHead(self):
        """ Remove the node at the head and return its data. """
        output = self.head.data
        if self.head.next == None:
            self.head = None
            self.tail = None
        else:
            self.head.next.previous = None
            self.head = self.head.next
        return output
        
    def removeTail(self):
        """ Remove the node at the tail and return its data. """
        output = self.tail.data
        if self.tail.previous == None:
            self.head = None
            self.tail = None
        else:
            self.tail.previous.next = None
            self.tail = self.tail.previous
        return output

    def isEmpty(self):
        """ Return True if the Deque is empty and False otherwise. """
        return self.head == None

    def delete(self, item):
        """ Delete all nodes in the Deque whose data is equal in value
        to that of item. """
        if item not in self:
            return "item not in dequeue"
        else:
            for node in self:
                if node.data == item:
                    wasHead = False
                    wasTail = False
                    if node == self.head:
                        self.removeHead()
                        wasHead = True
                    if node == self.tail:
                        self.removeTail()
                        wasTail = True
                    if not wasHead and not wasTail:
                        node.previous.next = node.next
                        node.next.previous = node.previous

    def __iter__(self):
        """ Iterator for Deque. """
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __contains__(self, item):
        """ Overloads the in operator so that we can ask if the item
        is in the Deque.  An item is in the Deque if there is a node
        with same value as that of item. """
        for node in self:
            if node.data == item: return True
        return False

    def __repr__(self):
        """ Returns the representation of the Deque. """
        output = ""
        for item in self:
            output += str(item.data) + " "
        if len(output) > 0:
            return output[:len(output)-1]
        else:
            return output
    
