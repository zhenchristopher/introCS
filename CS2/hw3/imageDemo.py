# Ran Libeskind-Hadas
# January 14, 2017
# imageDemo.py

# This file demonstrates the use of matplotlib's image tools and 
# numpy's fast arrays

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def demo():
    # Read the smallmonkey.png file into a numpy 2D array
    img=mpimg.imread(r'C:\Users\Zhenc_000\Documents\Caltech\CS2\hw3\smallmonkey.png')

    # Get the number of rows and columns in the image
    dimensions = img.shape
    rows = dimensions[0]
    columns = dimensions[1]

    # Notice the form of a pixel.  Its a np tuple of the form (r, g, b)
    # indicating the amount of red, green, and blue in that pixel,
    # each on a scale from 0.0 to 1.0
    print("The pixel at 50, 50 is:",img[50][50])

    # We are making a new numpy array, all entries initialized to zeros,
    # with the given number of rows and columns.  Each item in this array
    # is a floating point number rather than a tuple as above.
    # You could also make this an array of integers by using np.int
    # rather than np.float
    newImage = np.zeros((rows, columns), dtype = np.float)

    for r in range(rows):
        for c in range(columns):
            # You can see every pixel if you want!
            # print(img[r][c])  
            if img[r][c][0] > 0 or img[r][c][1] > 0 or img[r][c][2] > 0:
                newImage[r][c] = 1.0
                
    # Notice that newImage is an array of just 0's and 1's rather than
    # tuples.  That's fine!

    # Save the newImage as a .png file called newmonkey.png
    plt.imsave(r'C:\Users\Zhenc_000\Documents\Caltech\CS2\hw3\newmonkey1.png', newImage)

    # Now let's make a copy of that image and mess with it!
    newImageCopy = np.copy(newImage)
    for r in range(rows):
        for c in range(columns):
            newImageCopy[r][c] = 1.0 - newImageCopy[r][c]

    plt.imsave(r'C:\Users\Zhenc_000\Documents\Caltech\CS2\hw3\newmonkey2.png', newImageCopy)
    
    # Finally, let's build a new image that is just the left half of the
    # original monkey image.
    halfColumns = int(columns/2)

    # Construct a new array of the given dimensions with each element
    # being of the same type as that in the img (a np 3-tuple)

    halfMonkey = np.empty((rows, halfColumns, 3), img.dtype)
    for r in range(rows):
        for c in range(halfColumns):
            halfMonkey[r][c] = img[r][c]
    plt.imsave(r'C:\Users\Zhenc_000\Documents\Caltech\CS2\hw3\halfmonkey.png', halfMonkey)
    
    
demo()