import numpy as np

# Connect 4 Game Board

class Board:

    def __init__( self, width=7, height=6 ):
        """ the constructor for objects of type Board """
        self.width = width
        self.height = height
        self.data = [[' ']*width for r in range(height)]

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def __repr__(self):
        """ this method returns a string representation
            for an object of type Board
        """
        s = ''   # the string to return
        for row in range( self.height ):
            s += '|'   # add the spacer character
            for col in range( self.width ):
                s += self.data[row][col] + '|'
            s += '\n'
        s += '--'*self.width    # add the bottom of the board
        s += '-\n'
        for col in range( self.width ):
            s += ' ' + str(col%10)
        s += '\n'
        return s       # the board is complete, return it

    def addMove(self, col, ox):
        """ Add the game piece ox (either 'X' or 'O') to column col. """
        row = self.getHeight() - 1
        while self.data[row][col] != ' ':
            row -= 1
            if row < 0:
                return "invalid move"
        self.data[row][col] = ox

    def clear(self):
        """ Clear the game board of all game pieces. """
        self.data = [[' ']*width for r in range(height)]

    def setBoard(self, moves):
        """ Set the board using an input string representation. """
        pieces = "XO"
        xTurn = True
        for col in moves:
            if xTurn == True:
                self.addMove(int(col),'X')
                xTurn = False
            else:
                self.addMove(int(col),'O')
                xTurn = True

    def allowsMove(self, col):
        """ Return True if adding a game piece in the given column is 
            permitted and return False otherwise. """
        return self.data[0][col] == " "

    def isFull(self):
        """ Return True if the game board is full and False otherwise. """
        return not any(' ' in x for x in self.data)

    def delMove(self, col):
        """ Delete the topmost game piece from the given column. """
        for row in self.data:
            if row[col] != " ":
                row[col] = " "
                break

    def winsFor(self, ox):
        """ Return True if the game has been won by player ox where ox
            is either 'X' or 'O'. """
        gameWon = False
        for row in range(self.height):
            for col in range(self.width):
                if self.data[row][col] == ox:
                    gameWon = self.checkRow(row,col) or \
                        self.checkCol(row,col) or \
                        self.checkDiagDown(row,col) or \
                        self.checkDiagUp(row,col)
                    if gameWon:
                        break
            if gameWon:
                break
        return gameWon

    def checkRow(self,row,col):
        if col+3>=self.getWidth():
            return False
        return self.data[row][col] == self.data[row][col+1] and \
            self.data[row][col] == self.data[row][col+2] and \
            self.data[row][col] == self.data[row][col+3]

    def checkCol(self,row,col):
        if row+3>=self.getHeight():
            return False
        return self.data[row][col] == self.data[row+1][col] and \
            self.data[row][col] == self.data[row+2][col] and \
            self.data[row][col] == self.data[row+3][col]

    def checkDiagDown(self,row,col):
        if col+3>=self.getWidth() or row+3>=self.getHeight():
            return False
        return self.data[row][col] == self.data[row+1][col+1] and \
            self.data[row][col] == self.data[row+2][col+2] and \
            self.data[row][col] == self.data[row+3][col+3]

    def checkDiagUp(self,row,col):
        if col-3<0 or row+3>=self.getHeight():
            return False
        return self.data[row][col] == self.data[row+1][col-1] and \
            self.data[row][col] == self.data[row+2][col-2] and \
            self.data[row][col] == self.data[row+3][col-3]

# Connect 4 player

class Player:

    def __init__(self, ox, tbt, ply):
        self.symbol = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        output = ""
        output += "Player for "+self.symbol+"\n"
        output += "  with tiebreak: " + self.tieRule+"\n"
        output += "  and ply == " + str(self.ply)+"\n"
        return output
    
    def oppChar(self):
        """ Return the opposite game piece character. """
        if self.symbol == "O": return "X"
        else: return "O"

    def scoreBoard(self, b):
        """ Return the score for the given board b."""
        if b.winsFor(self.ox):
            return float(100)
        elif b.winsFor(self.oppChar()):
            return float(0)
        else:
            return float(50)

    def tiebreakMove(self, scores):
        """ Return column number of move based on self.tbt. """
        maximum = max(scores)
        maxList = [i for i in range(len(scores)) if scores[i]==maximum]
        if self.tbt == "LEFT":
            return maxList[0]
        if self.tbt == "RIGHT":
            return list(reversed(maxList))[0]
        if self.tbt == "RANDOM":
            return np.random.choice(maxList)

    def scoresFor(self, board):
        """ Return a list of scores for board, one score for each column
            of the board. """
        scores = [50] * b.getWidth()
        for col in range(len(scores)):
            if board.allowsMove(col) == False:
                scores[col] = -1
            elif board.winsFor(self.symbol):
                scores[col] = 100
            elif board.winsFor(self.oppChar()):
                scores[col] = 0
            elif self.ply == 0:
                scores[col] = 50
            else:
                board.addMove(col, self.symbol)
                newPlayer = Player(self.oppChar(),self.tbt, self.ply-1)
                scores[col] = 100 - max(newPlayer.scoresFor(board))
                board.delMove(col)
        return scores

    def nextMove(self, b):
        """ Takes a board as input and returns the next move for this player
            where a move is a column in which the player should place its
            game piece. """
        return self.tiebreakMove(self.scoresFor(b))

b = Board(7,6)
b.setBoard('1211244445')
print(b)
print(Player('X', 'RANDOM', 2).nextMove(b))
