import copy as cp
from testRNA import*

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
		
def fold5(RNAstring, memo={}):
	'''Returns the number of bonds in the optimal bonding pattern of the RNA string if we need bases to be 5 indices apart to bond'''
	if RNAstring in memo:
		return memo[RNAstring]
	elif len(RNAstring) == 0 or len(RNAstring) == 1:
		return 0 #base case
	else:
		best_solution = 0
		pair = 0
		for i in range(1,len(RNAstring)):
			if isComplement(RNAstring[0],RNAstring[i]) and i>=5: #added distance of 5 condition
				testString = [RNAstring[1:i],RNAstring[i+1:]] #create strings of inside and outside RNAstring
				test_solution = 1 + cp.copy(fold5(testString[0],memo) + fold5(testString[1],memo)) #find the total solution of this base pairing and the inside/outside strings
				if test_solution > best_solution:
					best_solution = test_solution
					pair = i
		if pair == 0: #if current base has no pairings, force a skip
			solution = fold5(RNAstring[1:],memo)
		else:
			solution = max(fold5(RNAstring[1:],memo),best_solution) #use maximum between use-it and lose-it
		memo[RNAstring] = solution
		return solution
		
print(fold5(testRNA))