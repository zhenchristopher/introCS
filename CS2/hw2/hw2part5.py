import turtle
import copy as cp
from testRNA import*
from operator import itemgetter

def draw_sec(RNA,matches):
	'''draws a small section of the matches that are in the same loop'''
	length = 500
	y_dist = 1
	for i in reversed(range(len(matches))):
		turtle.setx((matches[i][0]*length/(len(RNA)-1))-length/2)
		turtle.pendown()
		turtle.right(90)
		turtle.forward(20*y_dist) #change the length such that outermost base pairs can be differnetiated from the innermost ones
		turtle.left(90)
		turtle.forward(((matches[i][1]-matches[i][0])*length/(len(RNA)-1)))
		turtle.left(90)
		turtle.forward(20*y_dist)
		turtle.right(90)
		turtle.penup()
		y_dist += 1

def render(RNA,matches):
	'''given and RNA sequence and paris of binded bases, draws the backbone and the pairs'''
	length = 500
	turtle.setx(-250)
	turtle.pendown()
	turtle.forward(length)
	turtle.left(180)
	turtle.penup()
	turtle.forward(length)
	turtle.left(180)
	for i in range(0,len(RNA)-1): #draw RNA backbone
		turtle.dot(5,"blue")
		turtle.write(RNA[i],font = ("arial",16,"normal"))
		turtle.forward(length/(len(RNA)-1))
	turtle.dot(5,"blue")
	turtle.write(RNA[len(RNA)-1],font = ("arial",16,"normal"))
	turtle.pencolor("red")
	start_list = 0
	for i in range(1,len(matches)):
		if matches[i][1] > matches[i-1][1]: #divide the matches into individual loops
			draw_sec(RNA,matches[start_list:i])
			start_list = i
		if i == len(matches)-1: #draw the last loop
			draw_sec(RNA,matches[start_list:i+1])
	turtle.done()
	
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
	
def showStruct(RNA):
	'''generates and optimal structure and draws it for an RNA sequence'''
	render(RNA,getStruct(RNA)[1])
	
showStruct('AAGGGGUU')