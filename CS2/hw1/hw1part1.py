# Chris Zhen
# January 10, 2017
# This file contains my solutions for assignment 1, part 1

def dot(L,K):
	'''returns the dot product of lists L and K'''
	if L == [] or K == []:
		return 0.0
	return L[0]*K[0] + dot(L[1:],K[1:])

def explode(S):
	'''takes a string and returns each character of the string'''
	if S == '':
		return []
	return [S[0]] + explode(S[1:])
	
def ind(e,L):
	'''finds the index of an element in the list/string'''
	if L == '' or L == []:
		return 0
	if e == L[0]:
		return 0
	return 1 + ind(e,L[1:])

def removeAll(e,L):
	'''removes all top-level elements e in the list'''
	if L == []:
		return []
	if L[0] != e:
		return [L[0]] + removeAll(e,L[1:])
	return removeAll(e,L[1:])
	
def deepReverse(L):
	'''reverses the order of the list and all nested lists'''
	if L == []:
		return []
	if type(L[0]) == list:
		return deepReverse(L[1:]) + [deepReverse(L[0])]
	else:
		return deepReverse(L[1:]) + [L[0]]
		
def deepRemoveAll(item,L):
	'''removes all (not just top-level) elements e in the list'''
	if L == []:
		return []
	if type(L[0]) == list:
		return [deepRemoveAll(item,L[0])] + deepRemoveAll(item,L[1:])
	else:	
		if L[0] != item:
			return [L[0]] + deepRemoveAll(item,L[1:])
		return deepRemoveAll(item,L[1:])