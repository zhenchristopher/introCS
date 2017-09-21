# Christopher Zhen
# Feburary 7, 2017
# skworm.py

# This file has the classes required to play the Skworm game

# Basic scaffolding for skworm game

import tkinter
import random as rand
import numpy as np

SCREENWIDTH = 1000  # Width of the screen, in pixels
SCREENHEIGHT = 500  # Height of the screen, in pixels
COLUMNS = 100       # Width in worm cells
ROWS = 50           # Height in worm cells

# Although the screen is SCREENWIDTH x SCREENHEIGHT pixels, you'll be best off thinking about the screen
# as a grid that is COLUMNS x ROWS and each cell in that grid is therefore of width SCREENWIDTH/COLUMNS by
# SCREENHEIGHT/ROWS.  It will be nice to represent all worm body parts and food morsels in grid coordinates.
# But, when you write the render method at the bottom of this file, you'll be drawing in pixel coordinates.
# So, render will need to transform from grid coordinates (your internal representation) to pixel coordinates.

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

# The Worm class defines a worm.  
class Worm:
    def __init__(self):
        # self.body = Deque.Deque()  <-- This is how we will represent a worm!  You'll now need to add some body parts to this body.
        # Each body part can be a tuple of the form (row, col) which encodes the location of that body part.
        # You may also wish to set the worm's direction of movement and other useful attributes of the worm.
        worm = list(range(45,56)) #initialize body of worm
        self.body = Deque()
        for x in worm:
            self.body.addHead((x,25))
        self.lead = "head" #which side is leading the worm
        self.facing = np.array((1,0)) #direction that worm is headed
        self.flipping = False #whether in process of flipping
        self.eat = False #whether in process of eating
        self.dead = False #alive or dead

    def step(self):
        """ This method is called to have the worm update itself after
        taking one step. """
        # This method simply updates the worm's location by updating the Deque that represents its body.
        # In particular, you may want to remove its old tail and give it a new head!  You don't need or want
        # to change every body part because most of them stay the same!
        if self.flipping == True: #flipping head and tail
            if self.lead == "head":
                self.lead = "tail"
                if not self.eat: self.body.removeHead()
                direction = np.array(self.body.tail.data)-np.array(self.body.tail.previous.data)
            else:
                self.lead = "head"
                if not self.eat: self.body.removeTail()
                direction = np.array(self.body.head.data)-np.array(self.body.head.next.data)
            self.flipping = False
            self.facing = direction
            self.move(direction)
        else:
            if self.lead == "head":
                #remove the tail if not eating and move forward
                if not self.eat: self.body.removeTail()
                self.move(self.facing)
            else:
                if not self.eat: self.body.removeHead()
                self.move(self.facing)
        self.eat = False

    def move(self,direction):
        ''' This method is used to move the worm forward'''
        if self.lead == "head":
            newPiece = tuple(np.array(self.body.head.data)+direction)
            if newPiece in self.body: #die if we run into body
                self.dead = True
            elif newPiece[0]==-1 or newPiece[1]==-1 or newPiece[0]==COLUMNS or newPiece[1]==ROWS:
                self.dead = True
            self.body.addHead(newPiece)
        else:
            newPiece = tuple(np.array(self.body.tail.data)+direction)
            if newPiece in self.body:
                self.dead = True
            self.body.addTail(newPiece)

        
class Food:
    def __init__(self, howMuch):
        # This constructs a Deque of howMuch food items.  Each item is an ordered pair giving the grid location of the food item.
        # self.food = Deque.Deque() <-- This is where we will store food coordinates!
        worm = list(range(45,56))
        self.food = Deque()
        self.eaten = None #which food piece was eaten
        for x in range(howMuch):
            #make sure the food is not generated on the worm
            newFood = (rand.randint(0,100),rand.randint(0,50))
            while newFood[1] == 25 and newFood[0] in worm:
                newFood = (rand.randint(0,100),rand.randint(0,50))
            self.food.addHead(newFood)

    def step(self):
        """ This method is called to update the food on the board """
        # When this method is called, the oldest food item should be removed and a new food item should be introduced. 
        self.food.removeTail()
        self.food.addHead((rand.randint(0,100),rand.randint(0,50)))
        #remove the eaten food
        if self.eaten != None:
            # add an extra piece of food so we still have 50 pieces
            self.food.addHead((rand.randint(0,100),rand.randint(0,50)))
            self.food.delete(self.eaten)
        self.eaten = None

class Application(tkinter.Canvas):
 
    # The __init__ method sets up the graphics, registers the arrow keys
    # so that they respond when pressed, constructs a worm and food
    # and initializes the main loop.  You don't need to change anything here
    # other than uncommenting the two lines that are commented out.

    def __init__(self, root):
        tkinter.Canvas.__init__(self, root)
        
        self.screen = tkinter.Canvas(root, width=SCREENWIDTH, height=SCREENHEIGHT)
        self.screen.bind('<Left>', self.left_key)
        self.screen.bind('<Right>', self.right_key)
        self.screen.bind('<Up>', self.up_key)
        self.screen.bind('<Down>', self.down_key)
        
        self.screen.focus_set()
        self.screen.pack()

        self.delay = 100         # Set the delay in milliseconds.  You can adjust the speed of the game by altering this value.
        
        self.worm = Worm()     # This makes a new worm from the Worm class
        self.food = Food(50)   # This makes 50 food items

        # Call the timer method which will be invoked to refresh the 
        # screen every self.delay milliseconds.
        self.timer()             
             
    # You will need to have the four key options below do more than just 
    # print a message!  In particular, these methods can change a variable that governs
    # the direction that the worm will move!
    def left_key(self, event):
        direction = np.array((-1,0))
        #flip if we decide to go opposite direction
        if (direction == -1*self.worm.facing).all():
            self.worm.flipping = True
        else:
            self.worm.facing = direction
        print("Left key!")

    def right_key(self, event):
        direction = np.array((1,0))
        if (direction == -1*self.worm.facing).all():
            self.worm.flipping = True
        else:
            self.worm.facing = direction
        print("Right key!")

    def up_key(self, event):
        direction = np.array((0,-1))
        if (direction == -1*self.worm.facing).all():
            self.worm.flipping = True
        else:
            self.worm.facing = direction
        print("Up key!")

    def down_key(self, event):
        direction = np.array((0,1))
        if (direction == -1*self.worm.facing).all():
            self.worm.flipping = True
        else:
            self.worm.facing = direction
        print("Down key!")

    # Don't change timer.  This function will automatically be called
    # to clear the screen, call the step method below, and then
    # set the timer to do this again after self.delay milliseconds.
    
    def timer(self):
        self.screen.delete(tkinter.ALL)
        self.step()
        self.screen.after(self.delay, self.timer)

    # Change this!  This method will be called automatically by timer
    # to update the contents of the game screen.  It will 
    # call your self.worm.step() to make the worm update itself, then it 
    # will call your self.food.step() to update object to update the food contents
    # and then it will draw the contents of the board by calling the render method
    # that you will write below.
    def step(self):
        self.worm.step()
        self.food.step()
        headEat = self.worm.body.head.data in self.food.food
        tailEat = self.worm.body.tail.data in self.food.food
        #check if worm is eating food
        if headEat or tailEat:
            self.worm.eat = True
            if headEat:
                self.food.eaten = self.worm.body.head.data
            else:
                self.food.eaten = self.worm.body.tail.data
        #make sure no food is generated on worm
        for item in self.worm.body:
            self.food.food.delete(item.data)
        #check if worm is still alive
        if self.worm.dead:
            #if worm is dead, reinitialize the worm
            self.worm = Worm()
        self.render()

    # This function will be called by step to do the actual drawing.
    # Right now, it just renders a blue square at x=50, y=100 with 
    # size 10x10.  This function looks at the worm's body and draws it on the screen.
    # Then, it looks at the food locations (in the food Deque) and draws those on the screen.

    def render(self):
        for piece in self.worm.body:
            #color the head of the worm purple
            if self.worm.lead == "head":
                if piece == self.worm.body.head:
                    color = "purple"
                else:
                    color = "blue"
            else:
                if piece == self.worm.body.tail:
                    color = "purple"
                else:
                    color = "blue"
            x = 10*np.array(piece.data)[0]
            y = 10*np.array(piece.data)[1]
            #color the rest of the worm blue
            self.screen.create_rectangle(x, y, x+10, y+10, fill = color)
        for piece in self.food.food:
            #color the food red
            x = 10*np.array(piece.data)[0]
            y = 10*np.array(piece.data)[1]
            self.screen.create_rectangle(x, y, x+10, y+10, fill = "red")

root = tkinter.Tk()
app = Application(root)
app.mainloop()
