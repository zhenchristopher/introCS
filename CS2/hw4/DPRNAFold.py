# Christopher Zhen
# January 31, 2017
# DPRNAFold.py

# This file implements our folding and getStruct functions using
# dynamic programming

import numpy as np

def isComplement(base1,base2):
    """Returns boolean indicating if 2 RNA bases are complementary."""
    if base1=="A" and base2=="U":
        return True
    elif base1=="U" and base2=="A":
        return True
    elif base1=="C" and base2=="G":
        return True
    elif base1=="G" and base2=="C":
        return True
    if base1=="G" and base2=="U":
        return True
    elif base1=="U" and base2=="G":
        return True
    else:
        return False

def foldDP(RNA):
	'''Returns float indicating the maximum number of bonds in the RNA string without pseudoknots'''
	DParray = np.zeros([len(RNA),len(RNA)])
	for b in range(len(RNA)-1):
	#start by filling in base-pairs that are one away and build up from there
		i = 0
		for j in range(b+1,len(RNA)):
			poss_sol = 0
			if isComplement(RNA[i],RNA[j]):
				poss_sol = 1 + DParray[i+1,j-1] #if the two base pairs are complements, add 1 to the square on the left,down diagonal and save that as a possible solution
			DParray[i,j] = max(poss_sol, DParray[i+1,j], DParray[i,j-1]) #let the square be the maximum of either the left, lower (both lose-it cases), and use-it value
			i += 1 #iterate along diagonals
			j += 1
	return DParray[0,len(RNA)-1]
	
def getStructDP(RNA):
	'''Returns care package of both number of bonds and bond indices in the RNA string'''
	DParray = [[(0,[])]*(len(RNA)) for i in range(len(RNA))]
	for b in range(len(RNA)-1):
		i = 0
		for j in range(b+1,len(RNA)):
			poss_sol = (0,[])
			if isComplement(RNA[i],RNA[j]) and abs(i-j)>=5:
				poss_sol = (1 + DParray[i+1][j-1][0],[(i,j)] + DParray[i+1][j-1][1]) #now store a tuple instead of just bonds
			DParray[i][j] = max(poss_sol, DParray[i+1][j], DParray[i][j-1])
			i += 1
			j += 1
	return DParray[0][len(RNA)-1]