# Christopher Zhen
# January 24, 2017
# seam.py

# This file takes a user-defined image and shrinks it by a user-defined
# number of columns and finally saves it under a user-defined name

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import sys
import time
	
def gradCalc(a,b):
	'''function to calculate the color distance between two points'''
	return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)
	
def gradHelper(a,i,j,image):
	'''function to calculate the color gradient at a single point'''
	if a == 'x': #calc x-gradient
		if j == 0: #if at left boundary
			return gradCalc(image[i][j],image[i][j+1])
		elif j == image.shape[1] - 1: #if at right boundary
			return gradCalc(image[i][j],image[i][j-1])
		else:
			return gradCalc(image[i][j+1],image[i][j-1])
	if a == 'y': #calc y-gradient
		if i == 0: #if at bottom boundary
			return gradCalc(image[i][j],image[i+1][j])
		elif i == image.shape[0] - 1: #if at top boundary
			return gradCalc(image[i][j],image[i-1][j])
		else:
			return gradCalc(image[i+1][j],image[i-1][j])
	
def calcGradient(image):
	'''function to calculate the color gradient of the entire image'''
	dimensions = image.shape
	rows = dimensions[0]
	columns = dimensions[1]
	grad = np.array([[gradHelper('x',i,j,image) + gradHelper('y',i,j,image) for j in range(columns)] for i in range(rows)]) #create the gradient array
	return grad
	
def shrinkImage(image):
	'''function to use dynamic programming to find and remove the seam'''
	gradient = calcGradient(image)
	seams = seamCarve(gradient)
	return removeSeam(image,seams)

def seamCarve(gradient):
	'''use dynamic programming to find a seam from bottom up'''
	dimensions = gradient.shape
	rows = dimensions[0]
	columns = dimensions[1]
	cumCosts = [[(gradient[0,i],[(0,i)])]*columns for i in range(2)] #to start, let the row equal the energy of each element
	for i in range(1,rows): #for all other rows, set the cost equal to the gradient + the minimum cost of the below row (1 px away) and add the position to the current path
		for j in range(columns):
			below = (gradient[i,j]+cumCosts[0][j][0],[(i,j)]+cumCosts[0][j][1]) #cell directly below
			if j == 0: #if on left boundary
				belowr = (gradient[i,j]+cumCosts[0][j+1][0],[(i,j)]+cumCosts[0][j+1][1]) #cell below and to the right
				cumCosts[1][j] = min(below,belowr)
			elif j == columns - 1: #if on right boundary
				belowl = (gradient[i,j]+cumCosts[0][j-1][0],[(i,j)]+cumCosts[0][j-1][1]) #cell below and to the left
				cumCosts[1][j] = min(below,belowl)
			else:
				belowl = (gradient[i,j]+cumCosts[0][j-1][0],[(i,j)]+cumCosts[0][j-1][1]) #cell below and to the left
				belowr = (gradient[i,j]+cumCosts[0][j+1][0],[(i,j)]+cumCosts[0][j+1][1]) #cell below and to the right
				cumCosts[1][j] = min(below,belowl,belowr)
		cumCosts[0] = cumCosts[1] #replace the first row of cumCosts and repeat
	return min(cumCosts[1])[1]
	
def removeSeam(image,seam):
	'''removes the seam from the image for a seam that's written as a list of tuples of coordinates'''
	dimensions = image.shape
	rows = dimensions[0]
	columns = dimensions[1]
	newimage = np.empty((rows, columns-1, 3), image.dtype)
	for i in range(rows):
		pixDeleted = False
		for j in range(columns-1):
			if pixDeleted == False: #if the seam hasn't been encountered
				if (i,j) in seam: #if position is part of seam, don't add it to the new image
					pixDeleted = True
				else:
					newimage[i][j] = image[i][j] #if the coordinate is not part of the seam add it
			else:
				newimage[i,j-1:] = image[i,j:] #once the seam has been removed, add the remaining positions
				break
	return newimage

def main():
	'''function to remove the seams using input from the command line'''
	inputs = sys.argv
	image = mpimg.imread(inputs[1]) #source image filename/location
	newimage = inputs[2] #new image filename/location
	columns = eval(inputs[3]) #num of columns to be removed
	for i in range(columns):
		image = shrinkImage(image)
	plt.imsave(newimage,image)
	
if __name__ == '__main__': main()