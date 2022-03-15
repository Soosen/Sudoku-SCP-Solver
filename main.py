import arcade
import sys
import pyglet
import time
from sudoku import Sudoku
from sudokuGenerator import SudokuGenerator
from sudokuSolver import SudokuSolver

SCREEN_WIDTH = 800
SCREEN_HEIGHT = SCREEN_WIDTH
SCREEN_TITLE = "Sudoku SCP Solver"

#fps
UPDATE_RATE = 1/60

#chosen Monitor
MONITOR_NUM = 0
MONITORS = pyglet.canvas.Display().get_screens()
MONITOR = MONITORS[MONITOR_NUM]

#change that constant to generate a board with ELEMENTS_TO_REMOVE missing
ELEMENTS_TO_REMOVE = 60


class MyProject(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AZURE)

    def setup(self):

        #increase recursion limit
        sys.setrecursionlimit(30000)

        #set fps
        self.set_update_rate(UPDATE_RATE)

        #center the window on start
        self.center_on_screen()

        #create SudokuGenerator
        self.sudokuGenerator = SudokuGenerator()

        #generate a valid solved board
        startTime = time.time()
        self.sudokuGenerator.generateSudoku(self.sudokuGenerator.emptyBoard(), 0, 0)
        endTime = time.time()
        print("Generated in ", round((endTime - startTime) * 1000), " ms")

        #remove ELEMENTS_TO_REMOVE elements
        self.boardToSolve = self.sudokuGenerator.removeNumbers(self.sudokuGenerator.board, ELEMENTS_TO_REMOVE)

        #create SudokuSolver
        self.sudokuSolver = SudokuSolver()

        #pass the unsolved board to the Sudoku object in order to draw it
        self.sudoku = Sudoku(self.boardToSolve, SCREEN_WIDTH)
        self.sudoku.setConsantTiles(self.boardToSolve)

        #print(self.sudokuSolver.AC3(self.boardToSolve))

        pass

    def on_draw(self):
        #draw the maze
        self.clear()
        arcade.start_render()
        self.sudoku.draw()
        arcade.finish_render()


    def on_update(self, delta_time):

        pass
    def on_key_press(self, key, key_modifiers):

        #Key R - generate new sudoku board
        if key == arcade.key.R:
            startTime = time.time()
            self.sudokuGenerator.generateSudoku(self.sudokuGenerator.emptyBoard(), 0, 0)
            endTime = time.time()
            print("Generated in ", round((endTime - startTime) * 1000), " ms")
            self.boardToSolve = self.sudokuGenerator.removeNumbers(self.sudokuGenerator.board, ELEMENTS_TO_REMOVE)
            self.sudoku = Sudoku(self.boardToSolve, SCREEN_WIDTH)
            self.sudoku.setConsantTiles(self.boardToSolve)
        elif key == arcade.key.S:
            #Key S - solve the sudoku
            startTime = time.time()
            solved = self.sudokuSolver.solve(self.boardToSolve, 0 , 0, self.sudokuSolver.AC3(self.boardToSolve))
            #solved = self.sudokuSolver.solve(self.boardToSolve, 0 , 0)
            endTime = time.time()
            print("Solved in ", round((endTime - startTime) * 1000), " ms")
            self.sudoku.board = solved

            #Compare if the solved board is the same as the board that was generated at the first place. It doesnt have to be the case when there is more than one solution
            #to the board. The higher ELEMENTS_TO_REMOVE is the lower is the chance that solution is uniqe
            #print(SudokuSolver.compareBoards(solved, self.sudokuGenerator.board))
       
        pass

    def center_on_screen(self):
        _left = MONITOR.width // 2 - self.width // 2
        _top = (MONITOR.height // 2 - self.height // 2)
        self.set_location(_left, _top)

def main():
    project = MyProject(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    project.setup()

    arcade.run()




if __name__ == "__main__":
    main()