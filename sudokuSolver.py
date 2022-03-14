import math
import numpy
import random

SUDOKU_SIZE = 9
class SudokuSolver:

    #constraints
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

    #end constraints

    #chekc if a board is solved
    def isSolved(self, board):
        for i in range (9):
            for j in range (9):
                if(board[i][j] == 0):
                    return False
        
        return True

    #sovle a board
    def solve(self, board, curX ,curY):

        if(self.isSolved(board)):
            return board
        
        nextY = curY
        nextX = (curX + 1) % 9
        if((curX + 1) % 9 == 0):
            nextY = curY + 1 

        if(board[curX][curY] == 0):
            for i in range (9):
                if(not self.inRow(i + 1, curX, board) and not self.inColumn(i + 1, curY, board) and not self.inSquare(i + 1, curX, curY, board)):
                    board[curX][curY] = i + 1
                    copyBoard = numpy.copy(board)

                    result = self.solve(copyBoard, nextX, nextY)

                    if(result is not None):
                        return result
        else:
            copyBoard = numpy.copy(board)
            result = self.solve(copyBoard, nextX, nextY)

            if(result is not None):
                        return result

    #compares two borads, reurns true if they are exactly the same
    def compareBoards(boardA, boardB):
        for i in range(9):
            for j in range(9):
                if(boardA[i][j] != boardB[i][j]):
                    return False
        
        return True
    

    
