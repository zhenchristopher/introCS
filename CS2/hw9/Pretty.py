# Christopher Zhen
# March 7, 2017
# pretty.py

# Draw a pretty picture (Includes the vector, matrix, and shape classes)

import math
import turtle

class Matrix:
    """ 2x2 matrix class """

    def __init__(self, a11=0, a12=0, a21=0, a22=0):
        self.array = [[a11, a12], [a21, a22]]

    def set(self, row, column, value):
        """Set element at row and column to given value"""
        self.array[row][column] = value

    def get(self, row, column):
        """Get value at given row and column"""
        return self.array[row][column]

    def __add__(self, other):
        result = Matrix()
        for row in range(0, 2):
            for col in range(0, 2):
                result.set(row, col, self.get(row, col) + other.get(row, col))
        return result

    def __mul__(self, other):
        """ if other is a Matrix, returns a Matrix.  If other is a Vector, returns a Vector."""
        if other.__class__.__name__ == "Matrix":
            result = Matrix()
            for row in range(0, 2):
                for col in range(0, 2):
                    # Compute result matrix in the given row and col
                    entry = 0
                    for i in range(0, 2):
                            entry += self.get(row, i) * other.get(i, col)
                    result.set(row, col, entry)
            return result
        elif other.__class__.__name__ == "Vector":
            result = Vector()
            x = self.get(0, 0) * other.x + self.get(0, 1) * other.y
            y = self.get(1, 0) * other.x + self.get(1, 1) * other.y
            return Vector(x, y)
        else:
            print("Can't multiply a matrix by a ", other.__class__.name__, "!!!")  # !!! is a nice touch

    def __repr__(self):
        return str(self.array[0][0]) + " " + str(self.array[0][1]) + "\n" + str(self.array[1][0]) + " " + str(self.array[1][1])

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def magnitude(self):
        """ Returns magnitude of vector """
        return math.sqrt(self.x * self.x + self.y* self.y)

    def normalize(self):
        """ Sets vector magnitude to 1 """
        mag = self.magnitude()
        self.x = self.x/mag
        self.y = self.y/mag

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __neg__(self):
        """ This allows us to define a Vector v and then use the notation
        -v to get a new Vector which is the negation of the original! """
        return Vector(-self.x, -self.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, value):
        return Vector(self.x*value, self.y*value)

    def __repr__(self):
        return "Vector: (" + str(self.x) + "," + str(self.y) + ")"

class Shape:
    def __init__(self):
        self.points = []
        self.center = None
        
    def render(self):
        """Use turtle graphics to render shape"""
        turtle.penup()
        turtle.setposition(self.points[0].x, self.points[0].y)
        turtle.pendown()
        turtle.fillcolor(self.color)
        turtle.pencolor(self.color)
        turtle.begin_fill()
        for vector in self.points[1:]:
            turtle.setposition(vector.x, vector.y)
        turtle.setposition(self.points[0].x, self.points[0].y)
        turtle.end_fill()

    def erase(self):
        """Draw shape in white to effectively erase it from screen"""
        temp = self.color
        self.color = "white"
        self.render()
        self.color = temp
    
    def rotate(self, theta, about = Vector(0, 0)):
        """Rotate shape by theta degrees.  Please implement this
           by constructing the appropriate rotation matrix and then using
           that matrix to implement the rotation!"""
        theta = math.radians(theta) # math package uses radians, so we convert.
        R = Matrix(math.cos(theta),-1*math.sin(theta),math.sin(theta),math.cos(theta))
        # center the about point at the origin
        self.translate(Vector(0,0) - about)
        for i in range(len(self.points)):
            self.points[i] = R*self.points[i]
        self.translate(about)
        self.findCenter()

    def translate(self, shift):
        ''' Translate the shape by a shift vector '''
        for i in range(len(self.points)):
            self.points[i] = self.points[i] + shift
        self.findCenter()

    def scale(self, stretch):
        ''' Scale the shape by a given stretch scalar '''
        origCenter = self.findCenter()
        stretcher = Matrix(stretch,0,0,stretch)
        self.translate(Vector(0,0)-origCenter)
        for i in range(len(self.points)):
            self.points[i] = stretcher*self.points[i]
        self.translate(origCenter-Vector(0,0))
        self.findCenter()

    def flip(self, vector1, vector2):
        ''' Flips the shape with respect to a line defined by vector1 and 
        vector2 '''
        # First find the slope and intercept of the line
        slope = (vector1.y - vector2.y)/(vector1.x - vector2.x)
        intercept = vector1.y - (slope*vector1.x)
        # Rotate shape by theta to align the line with the x-axis
        self.rotate(360-1*math.degrees(math.atan(slope)), Vector(0, intercept))
        # Translate shape to place the line on the x-axis
        self.translate(Vector(0,-1*intercept))
        # Flip shape across x-axis
        flip = Matrix(1,0,0,-1)
        for i in range(len(self.points)):
            self.points[i] = flip*self.points[i]
        # Transform coordinates back to normal
        self.translate(Vector(0,intercept))
        self.rotate(math.degrees(math.atan(slope)), Vector(0, intercept))
        self.findCenter()

    def findCenter(self):
        ''' Finds the center of the shape and sets if '''
        center = Vector(0,0)
        for point in self.points:
            center += point
        self.center = center*(1/len(self.points))
        return self.center

class Compound(Shape):
    def __init__(self, center = Vector(0,0), shapeList = []):
        self.center = center
        self.shapeList = shapeList

    def render(self):
        for shape in self.shapeList:
            shape.render()

    def erase(self):
        for shape in self.shapeList:
            shape.erase()

    def translate(self, shift):
        for shape in self.shapeList:
            shape.translate(shift)
        self.center = self.center + shift

    def rotate(self, theta, about = Vector(0,0)):
        thetaD = math.radians(theta)
        R = Matrix(math.cos(thetaD),-1*math.sin(thetaD),math.sin(thetaD),math.cos(thetaD))
        self.translate(about*-1)
        for shape in self.shapeList:
            shape.rotate(theta)
        self.translate(about)

    def scale(self, stretch):
        for shape in self.shapeList:
            shape.scale(stretch)

    def flipx(self):
        ''' Helper funciton for flip, flips the compound across the x-axis '''
        for shape in self.shapeList:
            shape.flip(Vector(0,0),Vector(1,0))
        self.center = Matrix(1,0,0,-1) * self.center

    def flip(self, vector1, vector2):
        slope = (vector1.y - vector2.y)/(vector1.x - vector2.x)
        intercept = vector1.y - (slope*vector1.x)
        # Rotate shape by theta to align the line with the x-axis
        self.rotate(360-1*math.degrees(math.atan(slope)), Vector(0, intercept))
        # Translate shape to place the line on the x-axis
        self.translate(Vector(0,-1*intercept))
        # Flip shape across x-axis
        self.flipx()
        # Transform coordinates back to normal
        self.translate(Vector(0,intercept))
        self.rotate(math.degrees(math.atan(slope)), Vector(0, intercept))

    def findCenter(self):
        return self.center

    def append(self, shape):
        self.shapeList += [shape]

    def __add__(self, other):
        new = Compound()
        new.center = (self.center + other.center)*(1/2)
        new.shapeList = self.shapeList + other.shapeList
        return new


class Rectangle(Shape):
    def __init__(self, width, height, center = Vector(0, 0), color = "black"):
        SW = Vector(center.x - width/2.0, center.y - height/2.0)
        NW = Vector(center.x - width/2.0, center.y + height/2.0)
        NE = Vector(center.x + width/2.0, center.y + height/2.0)
        SE = Vector(center.x + width/2.0, center.y - height/2.0)
        self.points = [SW, NW, NE, SE]
        self.color = color
        self.center = center

class Square(Rectangle):
    def __init__(self, width, center=Vector(0, 0), color = "black"):
        Rectangle.__init__(self, width, width, center, color)
        
class Circle(Shape):
    def __init__(self, center = Vector(0, 0), radius = 10, color = "black"):
        self.points = [center] # Allow us to use the methods from Shape
        self.radius = radius
        self.color = color
        self.center = center

    def render(self):
        temp = self.center
        self.center = self.center - Vector(0, self.radius)
        turtle.penup()
        turtle.setposition(self.center.x, self.center.y)
        turtle.pendown()
        turtle.fillcolor(self.color)
        turtle.pencolor(self.color)
        turtle.begin_fill()
        turtle.circle(self.radius)
        turtle.end_fill()
        self.center = temp
        
    def scale(self, stretch):
        ''' Overload scale function '''
        self.radius = self.radius * stretch

class LineSegment(Shape):
    def __init__(self, v1, v2, color = "black"):
        self.points = [v1, v2]
        self.color = color

class Hex(Shape):
    ''' Draws a regular hexagon centered at the center with a "radius" of 
    radius '''
    def __init__(self, center = Vector(0,0), radius = 1, color = "black"):
        theta = math.radians(60)
        R = Matrix(math.cos(theta),-1*math.sin(theta),math.sin(theta),math.cos(theta))
        tempPoints = [Vector(0,radius)]
        for i in range(1,6):
            tempPoints += [R * tempPoints[i-1]]
        for i in range(6):
            tempPoints[i] = tempPoints[i] + center
        self.points = tempPoints
        self.center = center
        self.color = color

def demo():
    r = Square(40, Vector(0, 100), color="blue")
    for i in range(6):
        for j in range(6):
            r.render()
            r.rotate(60, r.center)
        r.scale(1.1)
        r.rotate(60)
    c = Hex(Vector(0, 250), 50, color = "red")
    for i in range(6):
        c.render()
        c.rotate(60)
        c.scale(0.8)   

def flipTest():
    xaxis = LineSegment(Vector(-50, 0), Vector(300, 0))
    yaxis = LineSegment(Vector(0, -50), Vector(0, 300))
    xaxis.render()
    yaxis.render()
    r = Rectangle(50, 100, Vector(0, 200), color = "red")
    r.render()
    flipLine = LineSegment(Vector(0, 50), Vector(250, 300), color = "blue")
    flipLine.render()
    r.flip(Vector(0, 50), Vector(250, 300))
    r.color = "green"
    r.render()

def compoundTest():
    s1 = Square(50, Vector(-50, 0), "red")
    s2 = Square(50, Vector(50, 0), "blue")
    group1 = Compound(Vector(-25, 0), [s1, s2])
    c1 = Circle(Vector(-50, 0), 20, "green")
    group2 = Compound(Vector(-25, 0), [c1])
    c2 = Circle(Vector(50, 0), 20, "black")
    group2.append(c2)
    group3 = group1 + group2
    group3.render()
    group3.rotate(90)
    group3.render()

def demo():
    s1 = Square(50, Vector(-100,0), "blue")
    s2 = Circle(Vector(0,0), 50, "red")
    s3 = Hex(Vector(100,0), 50, "green")
    s4 = LineSegment(Vector(-100,-100), Vector(100,100), "black")
    group1 = Compound(Vector(0,0), [s1, s3, s4])
    group1 += Compound(Vector(0,0), [s2])
    group1.render()
    group1.scale(0.5)
    group1.flip(Vector(-50,-50), Vector(50,50))
    group1.render()
    group1.rotate(90)
    group1.scale(0.5)
    group1.render()
    turtle.done()
