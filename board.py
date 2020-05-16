'''
The Board class stores the 2D list that is the representation of the chess board.
It also draws the board, which is called in the redrawAll of the main class.
'''

from tkinter import *
from PIL import Image, ImageTk


class Board(object):
    def __init__(self, width, board):
        self.width, self.size = width, width / 8
        # has to do with the mouse selection (used in main class)
        self.selectedPosition = (-1, -1)
        self.board = board

    # from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCell(self, x, y):
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        gridWidth = self.width
        gridHeight = self.width
        cellWidth = gridWidth / 8
        cellHeight = gridHeight / 8
        row = int(y / cellHeight)
        col = int(x / cellWidth)
        self.selectedPosition = (row, col)
        return row, col

    def draw(self, canvas):
        for row in range(8):
            for col in range(8):
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
                # drawing the checkerboard
                if (row + col) % 2 == 0:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='white')
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='tan')
                # only calling the draw method if the selected square has a piece
                if self.board[row][col] is not None:
                    self.board[row][col].draw(canvas)

    # from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCellBounds(self, row, col):
        margin = 8
        # aka 'modelToView'
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth = self.width - 2 * margin
        gridHeight = self.width - 2 * margin
        columnWidth = gridWidth / 8
        rowHeight = gridHeight / 8
        x0 = margin + col * columnWidth
        x1 = margin + (col + 1) * columnWidth
        y0 = margin + row * rowHeight
        y1 = margin + (row + 1) * rowHeight
        return x0, y0, x1, y1
