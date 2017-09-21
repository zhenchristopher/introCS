import time

def memoED(S1, S2, memo={}):
	'''Takes strings S1 and S2 as inputs and returns the edit distance between them.'''
	if (S1,S2) in memo:
		return memo[(S1,S2)]
	if len(S1) == 0:
		return len(S2)
	elif len(S2) == 0:
		return len(S1)
	elif S1[0] == S2[0]:
		solution = memoED(S1[1:],S2[1:],memo) #solution when S1[0] and S2[0] match
		memo[(S1,S2)] = solution
		return solution
	else:
		solution = min(1 + memoED(S1,S2[1:],memo), \
		1 + memoED(S1[1:],S2,memo), \
		1 + memoED(S1[1:],S2[1:],memo)) #best solution if the two don't match
		memo[(S1,S2)] = solution
		return solution
		
def main():
	f = open(r'C:\Users\Zhenc_000\Documents\Caltech\CS2\hw2\3esl.txt','r')
	words = f.read()
	wordList = words.split()
	print('The master word list contains {} words'.format(len(wordList)))
	while True:
		word = input('spell check> ') #ask for user inut
		matches = []
		start = time.time()
		for i in range(len(wordList)): #loop through all the words to find the minimum edit distances
			distance = memoED(word,wordList[i])
			if distance == 0:
				print("Correct")
				break
			matches += [(distance,wordList[i])]
		if len(matches)<len(wordList):
			continue
		end = time.time()
		print('Suggested alternatives:')
		matches.sort() #sort word list by edit distance from user input
		for i in range(10):
			print(matches[i][1])
		print("Total time : {} seconds".format(end-start))
		print("Average time per word: {} seconds".format((end-start)/len(wordList)))
	
main()