import copy as cp
from testRNA import*
from operator import itemgetter

def adjust(pairs, k):
	'''Returns a new array that adjusts each tuple in pairs by an integer k'''
	newpairs = []
	for i in range(0,len(pairs)):
		newpairs += [(pairs[i][0]+k,pairs[i][1]+k)] #shift pairs by k
	return newpairs
	
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
		
def getStruct(RNAstring, memo={}):
	'''Returns the number of bonds in the optimal bonding pattern of the RNA string and the structure of that bonding pattern'''
	if RNAstring in memo:
		return memo[RNAstring]
	elif len(RNAstring) == 0 or len(RNAstring) == 1:
		return (0,[]) #base case
	else:
		best_solution = (0,[])
		pair = 0
		for i in range(1,len(RNAstring)): #iterate through all following bases to find complementary ones
			if isComplement(RNAstring[0],RNAstring[i]) and i>=5:
				testString = [RNAstring[1:i],RNAstring[i+1:]] #create strings of inside and outside RNAstring
				inside = cp.copy(getStruct(testString[0],memo)) #find the structure of the inside and outside strings
				outside = cp.copy(getStruct(testString[1],memo))
				test_solution = (1 + inside[0] + outside[0], [(0,i)] + adjust(inside[1],1) + adjust(outside[1],i+1)) #find the total solution of this base pairing and the inside/outside strings
				if test_solution >= best_solution: #Tie betwen complementary bases goes to rightmost complementary base
					best_solution = test_solution
					pair = i
		shifted = cp.copy(getStruct(RNAstring[1:],memo))
		if pair == 0:
			memosolution = (shifted[0], adjust(shifted[1],0)) #memoize the unshifted pairing
			solution = (shifted[0], adjust(shifted[1],1)) #shift the indices if we skip a base
		else:
			memosolution = sorted([(shifted[0], adjust(shifted[1],0)), best_solution], key=lambda x: x[0])[1] #memoize unshifted
			solution = sorted([(shifted[0], adjust(shifted[1],1)), best_solution], key=lambda x: x[0])[1] #take the use-it if there's a tie between use it and lose it
		memo[RNAstring] = memosolution
		return solution
		
HIV = "AUAGGUACAGUAUUAGUAGGACCUACACCUGUCAACAUAAUUGGAAGAAAUAUGUUGACUCAGAUUGGUUGCACUUUAAAUUUUCCAAUUAGUCCUAUUGAAACUGUACCAGU"
print(getStruct(HIV))