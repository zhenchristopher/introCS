# Christopher Zhen
# January 31, 2017
# StackQ.py

# This file has the Stack and Queue classes with the methods completed

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

class Queue:
	def __init__(self):
		self.head = None  # The front of the queue is currently empty
		self.tail = None  # The end of the stack is currently empty
 
	# add a new Node with the given data to the tail of the queue
	def enqueue(self, data):
		newNode = Node(data)
		if self.isEmpty():
			self.head = newNode
			self.tail = newNode
		else:
			self.tail.next = newNode
			self.tail = newNode

	# remove the Node at the head of the queue and return its data
	def dequeue(self):
		if self.isEmpty():
			return None
		else:
			output = self.head.data
			if self.head == self.tail:
				self.head = None
				self.tail = None
			else:
				self.head = self.head.next
			return output

	# another name for enqueue; nothing for you to write here!
	def add(self, data):
		self.enqueue(data)

	# another name for dequeue; nothing for you to write here!
	def remove(self):
		return self.dequeue()

	# return True if the queue is empty and false otherwise
	def isEmpty(self):
		return self.head == None

	# return a nice string representation of the contents of the queue
	def __repr__(self):
		output = "Queue<"
		for item in self:
			output += str(item) + ", "
		if len(output) > 6:
			return output[:len(output)-2] + ">"
		else:
			return output + ">"
			
	def __iter__(self):
		currentNode = self.head
		while currentNode is not None:
			yield currentNode.data
			currentNode = currentNode.next