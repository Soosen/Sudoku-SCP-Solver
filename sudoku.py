import arcade
import numpy
SUDOKU_SIZE = 9

class Sudoku:
    def __init__(self, board, width):
        self.board = board
        self.width = width
        self.tile_size = width / SUDOKU_SIZE
        self.constant_tiles = numpy.zeros(shape = (SUDOKU_SIZE, SUDOKU_SIZE), dtype=int)

    #wraper function to draw a text in a tile with coordinates x,y
    def drawNumber(self, x, y, number, color):
         arcade.draw_text(str(number), (x + 0.3) * self.tile_size, (y + 0.25) * self.tile_size, color, 50)

    #draw the board     
    def draw(self):
        for i in range(SUDOKU_SIZE):
            thickness = 1

            if(i % 3 == 0):
                thickness = 3

            #horizontal
            arcade.draw_line(i * self.tile_size, 0, i * self.tile_size, self.width, arcade.color.BLACK, thickness)

            #vertical
            arcade.draw_line(0, i * self.tile_size, self.width, i * self.tile_size, arcade.color.BLACK, thickness)

        for i in range (SUDOKU_SIZE):
            for j in range (SUDOKU_SIZE):
                if(self.board[i][j] != 0):
                    if(self.constant_tiles[i][j] == 1):
                        #constant tiles                        
                        self.drawNumber(i, j, self.board[i][j], arcade.color.DEEP_CARMINE)
                    else:
                        #not constant tiles
                        self.drawNumber(i, j, self.board[i][j], arcade.color.BLACK)

    #save the positions of tiles that are constant in order to paint them in a different color
    def setConsantTiles(self, unsolvedBoard):
        constantTiles = numpy.zeros(shape = (SUDOKU_SIZE, SUDOKU_SIZE), dtype=int)

        for i in range(9):
            for j in range(9):
                if(unsolvedBoard[i][j] != 0):
                    constantTiles[i][j] = 1

        self.constant_tiles = constantTiles



               
