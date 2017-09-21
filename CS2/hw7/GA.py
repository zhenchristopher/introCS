# Picobot.py

import random
import numpy as np

# Dimensions of the board for the purposes of evolving Picobots
ROWS = 20
COLUMNS = 20

# Number of states in our Picobot programs
STATES = 5

# When evaluating a Picobot program for fitness, we run it TRIALS times (each time with
# a random starting location for STEPS steps.
TRIALS = 20
STEPS = 800

# The 9 possible patterns in an empty room
VALIDPATTERNS = ["xxxx", "Nxxx", "NExx", "NxWx", "xxxS", "xExS", "xxWS", "xExx", "xxWx"]

# The 4 possible directions
DIRECTIONS = ["N", "E", "W", "S"]

class Program:
    def __init__(self):
        self.rulesDict = {}

    def randomize(self):
        """ Constructs a random program """
        for state in range(STATES):
            for pattern in VALIDPATTERNS:
                rule = (state, pattern)
                newDirection = np.random.choice(DIRECTIONS)
                while newDirection in pattern:
                #make sure it's a valid direction
                    newDirection = np.random.choice(DIRECTIONS)
                newState = random.randint(0,STATES-1)
                self.rulesDict[rule] = (newDirection, newState)

    def getMove(self, state, pattern):
        """ Given a state and pattern string, returns a tuple of the form (newstate, move)
        indicating the move associated with that state and pattern."""
        return self.rulesDict[(state, pattern)]
    
    def mutate(self):
        """ Mutate the program by replacing one line of the program with another random line."""
        mutateState = random.randint(0,STATES-1)
        mutatePattern = np.random.choice(VALIDPATTERNS)
        rule = (mutateState, mutatePattern)
        newDirection = np.random.choice(DIRECTIONS)
        newState = random.randint(0,STATES-1)
        while newDirection in mutatePattern or newDirection in \
            self.rulesDict[rule] or newState in self.rulesDict[rule]:
            #make sure the move is valid and not the same as the one listed
            newDirection = np.random.choice(DIRECTIONS)
            newState = random.randint(0,STATES-1)
        self.rulesDict[rule] = (newDirection, newState)

    def crossover(self, other):
        """ Crosses self with other, returning a new program object """
        crossState = random.randint(0,STATES-1)
        newProgram = Program()
        for key in self.rulesDict:
            # create a new program with the first rules from self and the
            # rest from other
            if key[0] <= crossState:
                newProgram.rulesDict[key] = self.rulesDict[key]
            else:
                newProgram.rulesDict[key] = other.rulesDict[key]
        return newProgram

    def __repr__(self):
        output = ""
        for key in sorted(self.rulesDict.keys()):
            value = self.rulesDict[key]
            output = output + str(key[0]) + " " + str(key[1]) + " -> " + str(value[0]) + " " + str(value[1]) + "\n"
        return output
        
class Picobot:
    def __init__(self, picobotrow, picobotcol, program):
        self.numVisited = 1  # visited one cell so far
        self.position = (picobotrow, picobotcol)
        self.program = program
        self.state = 0
        self.roomState = np.zeros((ROWS,COLUMNS))
        # state of the room where 0 is unvisited and 1 is visited
        self.roomState[self.position[0], self.position[1]] = 1

    def step(self):
        """ Take one step in accordance with the current state and program """
        newMove = self.program.getMove(self.state, self.getPattern())
        self.state = newMove[1]
        if newMove[0] == "N":
            self.position = (self.position[0] - 1, self.position[1])
        elif newMove[0] == "S":
            self.position = (self.position[0] + 1, self.position[1])
        elif newMove[0] == "E":
            self.position = (self.position[0], self.position[1] + 1)
        else:
            self.position = (self.position[0], self.position[1] - 1)
        self.roomState[self.position[0],self.position[1]] = 1

    def getPattern(self):
        ''' Get the pattern sorrounding the bot (hard-coded for empty room)'''
        pattern = ""
        if self.position[0] == 0: pattern += "N"
        else: pattern += 'x'
        if self.position[1] == COLUMNS-1: pattern += "E"
        else: pattern += "x"
        if self.position[1] == 0: pattern += "W"
        else: pattern += "x"
        if self.position[0] == ROWS-1: pattern += "S"
        else: pattern += "x"
        return pattern

    def run(self, steps):
        """ Run the program for the given number of steps """
        for i in range(steps):
            self.step()

    def __repr__(self):
        """ Returns a string that displays the board, Picobot's location, and dots indicating
        spots that the the Picobot has visited. """
        disp = ""
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.roomState[row,col] == 0:
                    disp += " "
                else:
                    disp += "."
            disp += "\n"
        return disp

def GA(popSize, generations):
    ''' Main program for the genetic algorithm '''
    print("Grid size being used is ", ROWS, " by ", COLUMNS)
    print("Fitness is measured using", TRIALS, "random trials and running for", STEPS, "steps")
    population = []
    for bot in range(popSize):
        newProgram = Program()
        newProgram.randomize()
        fitness = evaluateFitness(newProgram)
        #use random number to break ties in fitness
        population += [(fitness, random.random(), newProgram)]
    for generation in range(generations+1):
        # sort the population by fitness
        population.sort(reverse=True)
        avgFitness = sum([x[0] for x in population])/popSize
        maxFitness = population[0][0]
        print("Generation " + str(generation) + "\n")
        print(" Average fitness: " + str(avgFitness) + "\n")
        print(" Best fitness: " + str(maxFitness) + "\n")
        if generation == generations:
            break
        population = nextGeneration(population, popSize)
    population.sort(reverse=True)
    print(population[0][2])

def evaluateFitness(program):
    ''' Evaluates the fitness of a program using TRIALS number of trials each
    with STEPS number of steps '''
    totalFitness = 0
    for trial in range(TRIALS):
        bot = Picobot(random.randint(0,ROWS-1),random.randint(0,COLUMNS-1)\
            ,program)
        bot.run(STEPS)
        totalFitness += sum(sum(bot.roomState))/(ROWS*COLUMNS)
    return totalFitness/TRIALS

def nextGeneration(population, popSize):
    ''' Creates the next generation of programs by taking the top half of 
    programs and randomly mating them to fill the population. Also randomly
    mutates half of the children programs '''
    newPopulation = population[:int(popSize/2)]
    while len(newPopulation) < popSize:
        parent1 = random.randint(0,int(popSize/2)-1)
        parent2 = random.randint(0,int(popSize/2)-1)
        while parent2 == parent1:
            # make sure parents aren't the same
            parent2 = random.randint(0,int(popSize/2)-1)
        # mate programs
        newProgram = population[parent1][2].crossover(population[parent2][2])
        if random.randint(0,1) == 1: newProgram.mutate()
        newFitness = evaluateFitness(newProgram)
        newPopulation += [(newFitness, random.random(), newProgram)]
    return newPopulation

# Run GA with popSize = 200 and 20 generations
GA(200,20)