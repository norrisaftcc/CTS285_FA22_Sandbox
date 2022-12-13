# Cell data class
from graphics import *
"""
Cells are the basic building blocks of the game. They are the squares that make up the grid.
Levels contain a 2D array of cells.
"""

class Cell:
    """ screens are drawn via cells for now.
    Each cell can contain a state"""
    def __init__(self, col, row, w, h, state = None, border = None, background = None, text=None):
        self.col = col
        self.row = row
        
        self.w = w
        self.h = h
        self.state = state
        self.border = border
        self.background = background
        self.text = text
        
class Level:
    def __init__(self, width, height, cellWidth=0, cellHeight=0, defaultBorder=None, defaultBackground=None):
        self.width = width
        self.height = height
        # extremely explicit description of this damn matrix
        # count across, this is the column number
        # cound down, this is the row number
        # we store a list of rows, each row is a list of cells
        # outer list is the rows, inner list is the columns of one row
        cols_count = width
        rows_count = height
        self.cells = [[0 for x in range(cols_count)] for y in range(rows_count)]
        
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.defaultBorder = defaultBorder
        self.defaultBackground = defaultBackground
        
    def getCellAt(self, row, col):
        """
        get the cell at the given position
        """
        return self.cells[row][col]     
        
    def makeLevel(self, cellWidth=None, cellHeight=None):
        # generate level
        # also, set the default cell properties (should probably go somewhere else?)
        # levels are a 2D array, width x height
        # we create them in read order (left to right, top to bottom)
        # <row, col>
        if cellWidth==None:
            cellWidth = self.cellWidth
        if cellHeight==None:
            cellHeight = self.cellHeight
        # create the cells
        for row in range(0, self.height):
            
            for col in range(0, self.width):
                # create new cell
                newCell = Cell(col, row, # position in the level
                                        self.cellWidth, self.cellHeight, # display size of the cell
                                        None, # state
                                        self.defaultBorder, self.defaultBackground)
                
                #self.cells[row][col] = newCell
                # insert in the appropriate location
                self.cells[row][col] = newCell
                assert newCell.col == col and newCell.row == row, "cell is not in the correct position"
                
    def labelCells(self, text = None):
        """
        label cells with their coordinates
        """
        for row in range(0, self.height):
            for col in range(0, self.width):
                thisCell = self.cells[row][col]
                assert isinstance(thisCell, Cell), "cell is not a Cell object"
                assert thisCell.col == col and thisCell.row == row, "cell is not in the correct position"
                # label this cell
                if text is None:
                    thisCell.text = str(col) + "," + str(row)
                else:
                    thisCell.text = text
                

    def draw(self):
        """
        render the level to the screen
        we draw cells in read order (left to right, top to bottom)
        """
        for row in range(0, self.height):
            for col in range(0, self.width):
                thisCell = self.getCellAt(row, col)
                assert isinstance(thisCell, Cell), "cell is not a Cell object"
                assert thisCell.col == col and thisCell.row == row, "cell is not in the correct position"
                # draw the cell
                x = thisCell.col * thisCell.w
                y = thisCell.row * thisCell.h
                cellWidth = thisCell.w
                cellHeight = thisCell.h
                if thisCell.background is not None:
                    draw_rectangle(x, y, cellWidth, cellHeight, thisCell.background)
                if thisCell.border is not None:
                    draw_rectangle_lines(x, y, cellWidth, cellHeight, thisCell.border)
                if thisCell.text is not None:
                    draw_text(thisCell.text, x + 10 , y + 10, 20, BLACK)
                
