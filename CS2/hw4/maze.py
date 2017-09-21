# Christopher Zhen
# January 31, 2017
# maze.py

# This file has all the files needed to implement BFS or DFS in solving a 
# user-defined maze.

import sys

# These are the symbols that represent the contents of a maze

EMPTY = '.'
WALL = '*'
FOOTSTEP = 'o'
START = 'S'
END = 'E'

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

class Maze():
	def __init__(self, array, start, end):
		""" start and end are ordered pairs in the form (row, column) """
		self.array = array
		self.start = start
		self.end = end
		self.rows = len(array)
		self.columns = len(array[0])

	def __repr__(self):
		output = ""
		for row in range(self.rows):
			for col in range(self.columns):
				output = output + " " + str(self.array[row][col])
			output = output + "\n"
		return output
			
def check(maze,cell):
	'''check the neighbor to see if it's empty'''
	if maze.array[cell[0]][cell[1]] == EMPTY:
		return [cell]
	else:
		return []

def neighbors(maze,cell):
	'''finds the empty neighbors of a cell and returns them as an array
	in the order of North, West, South, and East'''
	if cell[0] == 0:
		if cell[1] == 0:
			#check the south and east squares to see if they're empty
			neighbors = check(maze,(cell[0]+1,cell[1])) + check(maze,(cell[0],cell[1]+1))
		elif cell[1] == maze.columns - 1:
			#check the west and south squares
			neighbors = check(maze,(cell[0],cell[1]-1)) + check(maze,(cell[0]+1,cell[1]))
		else:
			#check the west, south, and east squares
			neighbors = check(maze,(cell[0],cell[1]-1)) + check(maze,(cell[0]+1,cell[1])) + check(maze,(cell[0],cell[1]+1))
	elif cell[0] == maze.rows - 1:
		if cell[1] == 0:
			#check north and east
			neighbors = check(maze,(cell[0],cell[1]-1)) + check(maze,(cell[0],cell[1]+1))
		elif cell[1] == maze.columns - 1:
			#check north and west
			neighbors = check(maze,(cell[0],cell[1]-1)) + check(maze,(cell[0]-1,cell[1]))
		else:
			#check north, west, and east
			neighbors = check(maze,(cell[0],cell[1]-1)) + check(maze,(cell[0]-1,cell[1])) + check(maze,(cell[0],cell[1]+1))
	else:
		if cell[1] == 0:
			#check north, south, and east
			neighbors = check(maze,(cell[0],cell[1]-1)) + check(maze,(cell[0]+1,cell[1])) + check(maze,(cell[0],cell[1]+1))
		elif cell[1] == maze.columns - 1:
			#check north, west, and south
			neighbors = check(maze,(cell[0],cell[1]-1)) + check(maze,(cell[0]-1,cell[1])) + check(maze,(cell[0]+1,cell[1]))
		else:
			#check north, west, south, and east
			neighbors = check(maze,(cell[0],cell[1]-1)) + check(maze,(cell[0]-1,cell[1])) + check(maze,(cell[0]+1,cell[1])) + check(maze,(cell[0],cell[1]+1))
	return neighbors
		
def search(maze, algName):
	""" Take a maze and a string as input.	algName is either DFS or BFS. """
	if algName == "DFS":
		S = Stack()
	else:
		S = Queue()
	visited = [maze.start]
	S.add(maze.start)
	previous = {} #dictionary of previous position (did this because our given Node class didn't have a previous method)
	while not S.isEmpty(): #using pseudocode from lecture
		cell = S.remove()
		if cell == maze.end:
			break
		for neighbor in neighbors(maze,cell):
			if neighbor in visited:
				continue
			else:
				S.add(neighbor)
				previous[neighbor] = cell
		visited += [cell]
	point = maze.end
	while point != maze.start: #find path back from the exit node
		maze.array[point[0]][point[1]] = FOOTSTEP
		point = previous[point]
	maze.array[maze.start[0]][maze.start[1]] = START
	maze.array[maze.end[0]][maze.end[1]] = END
	return maze
	
def readMaze(filename):
	""" Takes a string as input, opens that file, and returns a list of
	lists representing the maze. """
	f = open(filename, "r")	 # Open the file
	contents = f.read()		 # Read the contents
	f.close()				 # Close the file!
	rows = contents.split()
	mazeList = []
	for row in rows:
		mazeList.append(list(row))
	return mazeList		  

def main():
	""" The main function.	Gets the following arguments from the command
	line:  The filename containing the maze, the row and column of the start
	location, the row and column of the end position, and either DFS or BFS
	to indicate which of the two algorithms we're invoking."""
	inputs = sys.argv
	fileName = inputs[1]
	startRow = eval(inputs[2])
	startCol = eval(inputs[3])
	endRow = eval(inputs[4])
	endCol = eval(inputs[5])
	alg = inputs[6]	 # A string equal to "DFS" or "BFS"
	m = readMaze(fileName) #
	M = Maze(m, (startRow, startCol), (endRow, endCol))
	print(search(M, alg))

if __name__ == '__main__':
	main()