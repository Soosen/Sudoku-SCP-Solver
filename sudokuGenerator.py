import numpy
import random
import math

SUDOKU_SIZE = 9
class SudokuGenerator:
    def __init__(self):
        self.board = numpy.zeros(shape = (SUDOKU_SIZE, SUDOKU_SIZE), dtype=int)

    #constaints
    def inRow(self, number, row, board):
        for i in range (SUDOKU_SIZE):
            if(board[row][i] == number):
                return True
        
        return False

    def inColumn(self, number, column, board):
        for i in range (SUDOKU_SIZE):
            if(board[i][column] == number):
                return True
        
        return False

    def inSquare(self, number, row, column, board):
        for i in range (3):
            for j in range (3):
                if(board[i + math.floor(row / 3) * 3][j + math.floor(column / 3) * 3] == number):
                    return True
        
        return False

    #constraints end 
     
    #check if a board is fully generated 
    def isReady(self, board):
        for i in range (9):
            for j in range (9):
                if(board[i][j] == 0):
                    return False
        
        return True
      

    #generate a sequence of unique numbers 1-9 in a random order
    def randomSequence(self):
        seq = numpy.array([], dtype=int)

        while(seq.size != 9):
            r = random.randint(1,9)
            if(not numpy.isin(r,seq)):
                seq = numpy.append(seq, r)
        return seq

    #generate a valid solved sudoku board
    def generateSudoku(self, board, curX, curY):
        if(self.isReady(board)):
            self.board = board
            return board
        
        nextY = curY
        nextX = (curX + 1) % 9
        if((curX + 1) % 9 == 0):
            nextY = curY + 1 

        if(board[curX][curY] == 0):
            sequence = self.randomSequence()
            for i in range (9):
                index = sequence[i]
                if(not self.inRow(index, curX, board) and not self.inColumn(index, curY, board) and not self.inSquare(index, curX, curY, board)):
                    board[curX][curY] = index
                    copyBoard = numpy.copy(board)

                    result = self.generateSudoku(copyBoard, nextX, nextY)

                    if(result is not None):
                        self.board = result
                        return result
        else:
            copyBoard = numpy.copy(board)
            result = self.generateSudoku(copyBoard, nextX, nextY)

            if(result is not None):
                self.board = result
                return result


    #remove amount elements from a board
    def removeNumbers(self, board, amount):
        boardCopy = numpy.copy(board)
        for i in range(amount):
            x = random.randint(0,8)
            y = random.randint(0,8)

            while boardCopy[x][y] == 0:
                x = random.randint(0,8)
                y = random.randint(0,8)
            
            boardCopy[x][y] = 0
        return boardCopy

    #generate an empty board
    def emptyBoard(self):
        return numpy.zeros(shape = (SUDOKU_SIZE, SUDOKU_SIZE), dtype=int)

