import sys
import random
import time
import matplotlib.pyplot as plt

# The following is used to allow Python to do "a lot" of recursion.
# Without this, Python is likely to complain if your function tries to 
# make too many recursive calls.
sys.setrecursionlimit(30000)  

def mergesort(myList):
    ''' mergesort the given list '''
    if len(myList) <= 1: return myList
    else:
        midpoint = int(len(myList)/2)
        return merge(mergesort(myList[0:midpoint]),
                     mergesort(myList[midpoint:]))

def merge(sortedList1, sortedList2):
    ''' merge two sorted arrays '''
    if sortedList1 == []: return sortedList2
    elif sortedList2 == []: return sortedList1
    elif sortedList1[0] < sortedList2[0]: 
        return [sortedList1[0]] + merge(sortedList1[1:], sortedList2)
    else: 
        return [sortedList2[0]] + merge(sortedList1, sortedList2[1:])
                                  
def insert(x, L):
    ''' insert element x into sorted list L '''
    if L == []: return [x]
    elif x <= L[0]: return [x] + L
    else: return [L[0]] + insert(x, L[1:])

def insertionsort(myList):
    ''' insertion sort the given list '''
    if myList == []: return myList
    else: return insert(myList[0], insertionsort(myList[1:]))

def test(startLength,endLength,step,trials):
	'''test function for finding and graphing the computation times
	of mergesort and insertionsort'''
	trialx = list(range(startLength,endLength,step))
	mergetrials = []
	inserttrials = []
	for length in range(startLength,endLength,step):
		array = list(range(0,length))
		totmerge = 0
		totinsert = 0
		for iteration in range(trials):
			random.shuffle(array)
			start = time.time()
			mergesort(array)
			end = time.time()
			totmerge += (end-start)
			start = time.time()
			insertionsort(array)
			end = time.time()
			totinsert += (end-start)
		mergetrials += [totmerge/trials]
		inserttrials += [totinsert/trials]
	plt.plot(trialx,mergetrials, "ro")
	plt.plot(trialx,inserttrials, "bx")
	#plt.savefig("hw1part2.png")
	plt.show()
	
test(100, 500, 50, 20)