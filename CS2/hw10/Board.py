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
        row = self.getHeight()
        while self.data[row][col] != ' ':
            row += 1
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
        return self.data.index(" ") == -1

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
            return gameWon

    def checkRow(self,row,col):
        if col+4>=self.width:
            return False
        return self.data[row][col] == self.data[row][col+1] and \
            self.data[row][col] == self.data[row][col+2] and \
            self.data[row][col] == self.data[row][col+3] and \
            self.data[row][col] == self.data[row][col+4]

    def checkCol(self,row,col):
        if row+4>=self.height:
            return False
        return self.data[row][col] == self.data[row+1][col] and \
            self.data[row][col] == self.data[row+2][col] and \
            self.data[row][col] == self.data[row+3][col] and \
            self.data[row][col] == self.data[row+4][col]

    def checkDiagDown(self,row,col):
        if col+4>=self.width or row+4>=self.height:
            return False
        return self.data[row][col] == self.data[row+1][col+1] and \
            self.data[row][col] == self.data[row+2][col+2] and \
            self.data[row][col] == self.data[row+3][col+3] and \
            self.data[row][col] == self.data[row+4][col+4]

    def checkDiagUp(self,row,col):
        if col-4<0 or row+4>=self.height:
            return False
        return self.data[row][col] == self.data[row+1][col-1] and \
            self.data[row][col] == self.data[row+2][col-2] and \
            self.data[row][col] == self.data[row+3][col-3] and \
            self.data[row][col] == self.data[row+4][col-4]
