import math
import numpy
from collections import deque

SUDOKU_SIZE = 9
class SudokuSolver:

    #constraints for backtracking
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

    #constraints for AC3
    def constraintRow(self, varList, x, y):
        #if there is only one variable for a domain remove the variable from the entire row
        retCells = numpy.array([], dtype=object)
        if(varList[x][y].size == 1):
            for i in range(9):
                if(i != x):
                    index = numpy.argwhere(varList[i][y] == varList[x][y][0])
                    if(index.size != 0):
                        varList[i][y] = numpy.delete(varList[i][y], index[0])
                        retCells = numpy.append(retCells, Cell(i, y))

        return retCells

    
    def constraintColumn(self, varList, x, y):
        #if there is only one variable for a domain remove the variable from the entire column
        retCells = numpy.array([], dtype=object)
        if(varList[x][y].size == 1):
            for i in range(9):
                if(i != y):
                    index = numpy.argwhere(varList[x][i] == varList[x][y][0])
                    if(index.size != 0):
                        varList[x][i] = numpy.delete(varList[x][i], index[0])
                        retCells = numpy.append(retCells, Cell(x, i))

        return retCells

    def constraintSquare(self, varList, x, y):
        #if there is only one variable for a domain remove the variable from the entire 3x3 square
        retCells = numpy.array([], dtype=object)

        if(varList[x][y].size == 1):
            for i in range (3):
                for j in range (3):
                    curX = i + math.floor(x / 3) * 3
                    curY = j + math.floor(y / 3) * 3
                    if(curX != x and curY != y):
                        index = numpy.argwhere(varList[curX][curY] == varList[x][y][0])
                        if(index.size != 0):
                            varList[curX][curY] = numpy.delete(varList[curX][curY], index[0])
                            retCells = numpy.append(retCells, Cell(curX, curY))
        
        return retCells

    #end constraints

    #check if a board is solved
    def isSolved(self, board):
        for i in range (9):
            for j in range (9):
                if(board[i][j] == 0):
                    return False
        
        return True

    #create a list of all domains and their possible variables
    def createDomainsVariables(self, board):
        variablesList = numpy.empty((9,9), dtype=object)
        for i in range(9):
            for j in range(9):
                if(board[i][j] != 0):
                    variablesList[i][j] = numpy.array([board[i][j]])
                else:
                    variablesList[i][j] = numpy.array([1,2,3,4,5,6,7,8,9])

        return variablesList

    #concat two arrays
    def concatArrays(self, arrayA, arrayB):
        for b in arrayB:
            arrayA = numpy.append(arrayA, b)

        return arrayA
        
    #AC3 algorithm
    def AC3(self, board):

        varList = self.createDomainsVariables(board)
        q = deque([])

        for i in range(9):
            for j in range(9):
                q.append(Cell(i,j))

        while q:
            current = q.popleft()
            toAppend = numpy.array([], dtype=object)
            toAppend = self.concatArrays(toAppend, self.constraintRow(varList, current.x, current.y))
            toAppend = self.concatArrays(toAppend, self.constraintColumn(varList, current.x, current.y))
            toAppend = self.concatArrays(toAppend, self.constraintSquare(varList, current.x, current.y))

            if(toAppend.size != 0):
                for cell in toAppend:
                    q.append(cell)


        return varList


    #solve a board
    def solve(self, board, curX ,curY, possibleVariables):

        if(self.isSolved(board)):
            return board
        
        nextY = curY
        nextX = (curX + 1) % 9
        if((curX + 1) % 9 == 0):
            nextY = curY + 1 

        if(board[curX][curY] == 0):
            for i in range (possibleVariables[curX][curY].size):
                curValue = possibleVariables[curX][curY][i]
                if(not self.inRow(curValue, curX, board) and not self.inColumn(curValue, curY, board) and not self.inSquare(curValue, curX, curY, board)):
                    board[curX][curY] = curValue
                    copyBoard = numpy.copy(board)

                    result = self.solve(copyBoard, nextX, nextY, possibleVariables)

                    if(result is not None):
                        return result
        else:
            copyBoard = numpy.copy(board)
            result = self.solve(copyBoard, nextX, nextY, possibleVariables)

            if(result is not None):
                        return result



    #compares two borads, reurns true if they are exactly the same
    def compareBoards(boardA, boardB):
        for i in range(9):
            for j in range(9):
                if(boardA[i][j] != boardB[i][j]):
                    return False
        
        return True
    

class Cell(): 
    def __init__(self, x, y):
        self.x = x
        self.y = y

