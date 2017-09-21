# Christopher Zhen
# January 31, 2017
# twenty.py

# This file has the 20 questions game including the Node and BST classes and
# the ability to load and save games

class Node:
	'''node class for the binary search tree'''
	def __init__(self, data = None):
		self.data = data
		self.yesChild = None
		self.noChild = None
		self.parent = None
	
	#return whether the node is a leaf
	def isLeaf(self):
		return self.numChildren() == 0
	
	#return how many children the node has
	def numChildren(self):
		counter = 0
		if self.yesChild != None:
			counter += 1
		if self.noChild != None:
			counter += 1
		return counter
	
	#return whether the node is the root of a tree
	def isRoot(self):
		return self.parent == None
		
	#return whether the node is a yesChild
	def isYesChild(self):
		return self.parent.yesChild == self
		
	#return whether the node is a noChild
	def isNoChild(self):
		return self.parent.noChild == self
		
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
			return self.reprHelper(current.yesChild) + ' ' + str(current.data) + ' ' + self.reprHelper(current.noChild)
		
def buildTree(inputList):
	'''function that recursively takes in input list and returns the corresponding tree'''
	if inputList[1] == 'Leaf': #base case of leaf, return a node with the data
		currentTree = BSTSet()
		currentTree.root = Node(inputList[0])
		return [currentTree,inputList[2:]]
	else:
		currentTree = BSTSet() #set the root of the tree to be the first element
		newNode = Node(inputList[0])
		currentTree.root = newNode
		[tree, restOfInputList] = buildTree(inputList[2:])
		newNode.yesChild = tree.root #build everything on the left of the node and find what elements remain
		tree.root.parent = newNode
		[newTree, newRestOfInputList] = buildTree(restOfInputList)
		newNode.noChild = newTree.root #build everything on the right of the node with the remaining elements
		newTree.root.parent = newNode
		return [currentTree, newRestOfInputList] #return the complete tree as well as the remaining items of the input list
	
def saveTree(root):
	'''function that recursively takes the root of the tree and returns an input list'''
	if root.isLeaf(): #base case of leaf
		return [root.data, 'Leaf']
	else:
		return [root.data, 'Internal node'] + saveTree(root.yesChild) + saveTree(root.noChild) #add the root plus everything to the left and everything to the right
		
def play():
	'''main function to play the 20 questions game'''
	save = str(input('Would you like to load in a previous game? '))
	if save == 'no':
		default = BSTSet()
		default.root = Node('Is it bigger than a breadbox? ')
		default.root.yesChild = Node('elephant')
		default.root.noChild = Node('mouse')
		default.root.yesChild.parent = default.root
		default.root.noChild.parent = default.root
		game(default.root) #play the game with the default tree
	else:
		save = input('Enter a name for the file: ')
		game(loadGame(save).root) #play the game with a user-defined save
		
def game(root):
	'''rest of the game that can either play a saved game or play the default game'''
	currentNode = root
	while not currentNode.isLeaf(): #keep on asking questions until we're ready to guess
		if currentNode.data[len(currentNode.data)-1] != ' ': #add a space after a question if it's not already there
			currentNode.data += ' '
		answer = str(input(currentNode.data))
		if answer == 'yes':
			currentNode = currentNode.yesChild
		else:
			currentNode = currentNode.noChild
	if currentNode.data[0] in ['a','e','i','o','u','A','E','I','O','U']: #if we have a vowel starting the word, use 'an' instead of 'a'
		answer = str(input('Is it an ' + currentNode.data + '? '))
	else:
		answer = str(input('Is it a ' + currentNode.data + '? '))
	if answer == 'yes':
		print('Yay, I got it!')
	else:
		newLeaf = Node(str(input('Shucks!  What were you thinking of? ')))
		newNode = Node(str(input('Please give me a question for which the answer for a ' + newLeaf.data + ' would be YES and the answer for a ' + currentNode.data + ' would be NO: ')))
		#rearrange the tree with the newNode and newLeaf
		if currentNode.isYesChild():
			currentNode.parent.yesChild = newNode
		else:
			currentNode.parent.noChild = newNode
		newNode.parent = currentNode.parent
		newNode.yesChild = newLeaf
		newLeaf.parent = newNode
		newNode.noChild = currentNode
		currentNode.parent = newNode
	again = str(input('Would you like to play again? '))
	if again == 'yes':
		game(root) #play again with the same tree
	else:
		save = str(input('Would you like to save this game? '))
		if save == 'yes': #save file
			save_name = str(input('Enter a name for the file: '))
			saveGame(root,save)
		print('Goodbye!')
		return
			
def saveGame(root, save):
	'''uses the saveTree function to save the current tree to a user-defined file name'''
	file = open(save, 'w')
	inputList = saveTree(root)
	for item in inputList:
		file.write(item + '\n')
	file.close()
			
def loadGame(save):
	'''uses the buildTree function to read a user-defined save file and return the tree'''
	file = open(save, 'r')
	inputList = file.read().splitlines() #read the file without the \n characters
	file.close
	return buildTree(inputList)[0]

play()