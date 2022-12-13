# Cell data class
from graphics import *
"""
Cells are the basic building blocks of the game. They are the squares that make up the grid.
Levels contain a 2D array of cells.

In Maze, cells are either linked or unlinked with their neighbors.
Linked cells allow travel between them.
"""

class Cell:
    """ screens are drawn via cells for now.
    Each cell can contain a state"""
    def __init__(self, col, row, w, h, state = None, border = None, background = None, text=None):
        self.col = col
        self.row = row
        
        self.w = w
        self.h = h
        self.state = None
        self.border = border
        self.background = background
        self.text = text
    
    def __str__(self):
        return "Cell: "  + str(self.row) + ", "  + str(self.col) + "->" + str(self.state)
        
        

class Exits:
    """ Exits are the connections between cells.
    They can be linked or unlinked.
    We're using composition rather than inheritance here.
    """
    def __init__(self):
        # directions are linked or unlinked (or None, cannot link)
        self.north = False
        self.south = False
        self.east = False
        self.west = False
        # destinations are the cells that the exits lead to
        self.northDest = None
        self.southDest = None
        self.eastDest = None
        self.westDest = None
    
    def __str__(self):
        return "" + "/N:" + str(self.north) + "/S:" + str(self.south) + "/E:" + str(self.east) + "/W:" + str(self.west)
        
    def link(self, direction, bidi = True):
        """ link an exit to a direction """
        if direction == "north" and self.north != None:
            self.north = True
        elif direction == "south" and self.south != None:
            self.south = True
        elif direction == "east" and self.east != None:
            self.east = True
        elif direction == "west" and self.west != None:
            self.west = True
        else:
            assert False, "Invalid direction or illegal link"
        
        # we set up destinations in the level class, not here

        if bidi:
            # bidi links are two-way, so we need to link the destination cell as well
            # we need to know the destination cell to do this
            # don't bidi link infinitely, so return links are not bidi
            if direction == "north" and self.north == True:
                self.northDest.state.link("south", False)
            if direction == "south" and self.south == True:
                self.southDest.state.link("north", False)
            if direction == "east" and self.east == True:
                self.eastDest.state.link("west", False)
            if direction == "west" and self.west == True:
                self.westDest.state.link("east", False)
        
    

class MazeLevel:
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
                # set up links
                newCell.state = Exits()
                # can't ever link out of bounds (an exit that would be off the edge of the level)
                if row == 0:
                    newCell.state.north = None 
                if row == self.height - 1:
                    newCell.state.south = None 
                if col == 0:
                    newCell.state.west = None 
                if col == self.width - 1:
                    newCell.state.east = None 
                
                # insert in the appropriate location
                self.cells[row][col] = newCell
                assert newCell.col == col and newCell.row == row, "cell is not in the correct position"
                    
        # second pass - set destinations (since all cells now exist)
        for row in range(0, self.height):
            for col in range(0, self.width):
                currentCell = self.getCellAt(row, col)
                # assert the currentCell is a Cell
                assert isinstance(currentCell, Cell), "cell is not a Cell object"
                # assert the currentCell is in the correct position
                assert currentCell.col == col and currentCell.row == row, "cell is not in the correct position"
                # set up destinations
                if currentCell.state.north == False:
                    currentCell.state.northDest = self.getCellAt(row-1, col)
                if currentCell.state.south == False:
                    currentCell.state.southDest = self.getCellAt(row+1, col)
                if currentCell.state.east == False:
                    currentCell.state.eastDest = self.getCellAt(row, col+1)
                if currentCell.state.west == False:
                    currentCell.state.westDest = self.getCellAt(row, col-1)
                # now assuming our destinations are valid, links will work
                
                
                
                
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
        fontSize = 12
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
                    draw_rectangle(x+1, y+1, cellWidth-1, cellHeight-1, thisCell.background)
                if thisCell.border is not None:
                    draw_rectangle_lines(x+1, y+1, cellWidth-1, cellHeight-1, thisCell.border)
                    draw_rectangle_lines(x, y, cellWidth, cellHeight, thisCell.border) # 2 pixel width border
                if thisCell.text is not None:
                    draw_text(thisCell.text, x + 1 + cellWidth // 4 , y + 1 + cellHeight // 4, fontSize, DARKGRAY)
                # draw the cell's exits
                # we should shrink the drawn cell size to avoid overlaps
                # calculate the exit size: 1/4 of the cell size 
                #topExitSize = cellWidth // 4
                #sideExitSize = cellHeight // 4
                # consider doors as holes in the walls of a cell that open it to neighbors
                topDoorSize = int (cellWidth * 0.8)
                topDoorWidth = 2
                sideDoorSize = int (cellHeight * 0.8)
                sideDoorWidth = 2
                # for reference:
                # the north exit spans from coordinates (x, y) to (x + cellWidth, y + exitSize)
                # the south exit spans from coordinates (x, y + cellHeight - exitSize) to (x + cellWidth, y + cellHeight)
                # the east exit spans from coordinates (x + cellWidth - exitSize, y) to (x + cellWidth, y + cellHeight)
                # the west exit spans from coordinates (x, y) to (x + exitSize, y + cellHeight)
                exitColor = self.defaultBackground
                DEBUG_WALLS = False
                if DEBUG_WALLS == False:
                    # draw walls using the background color
                    if thisCell.state.north == True:
                        #draw_line(x+1, y+1, x + cellWidth-1, y-1, RED)
                        #draw_line(x+topExitSize, y+1, x + cellWidth-topExitSize, y+1, exitColor)
                        #draw_rectangle(x+topExitSize, y, cellWidth-topExitSize*2, 2, exitColor)
                        #draw the exit from the center of the north wall, reaching topExitSize/2 pixels each direction
                        draw_rectangle((x + cellWidth // 2 - topDoorSize // 2), y, topDoorSize, topDoorWidth, exitColor)
                    if thisCell.state.south == True:
                        #draw_line(x+topExitSize, y + cellHeight-1, x + cellWidth-topExitSize, y + cellHeight-1, exitColor)
                        #draw_rectangle(x+topExitSize, y + cellHeight-2, cellWidth-topExitSize*2, 2, exitColor)
                        #draw the exit from the center of the south wall, reaching topExitSize/2 pixels each direction
                        draw_rectangle((x + cellWidth // 2 - topDoorSize // 2), y + cellHeight - topDoorWidth, topDoorSize, topDoorWidth, exitColor)
                    if thisCell.state.east == True:
                        #draw_line(x + cellWidth-1, y+sideExitSize, x + cellWidth-1, y + cellHeight-sideExitSize, exitColor)
                        #draw_rectangle(x + cellWidth-2, y+sideExitSize, 2, cellHeight-sideExitSize*2, exitColor)
                        #draw the exit from the center of the east wall, reaching sideExitSize/2 pixels each direction
                        draw_rectangle(x + cellWidth - sideDoorWidth, y + cellHeight // 2 - sideDoorSize // 2, sideDoorWidth, sideDoorSize, exitColor)
                    if thisCell.state.west == True:
                        #draw_line(x+1, y+sideExitSize, x+1, y + cellHeight-sideExitSize, exitColor)
                        #draw_rectangle(x, y+sideExitSize, 2, cellHeight-sideExitSize*2, exitColor)
                        #draw the exit from the center of the west wall, reaching sideExitSize/2 pixels each direction
                        draw_rectangle(x, y + cellHeight // 2 - sideDoorSize // 2, sideDoorWidth, sideDoorSize, exitColor)
                else:
                    # draw each exit using a different color
                    if thisCell.state.north == True:
                        #draw_line(x+1, y+1, x + cellWidth-1, y-1, RED)
                        #draw_line(x+topExitSize, y+1, x + cellWidth-topExitSize, y+1, exitColor)
                        #draw_rectangle(x+topExitSize, y, cellWidth-topExitSize*2, 2, exitColor)
                        #draw the exit from the center of the north wall, reaching topExitSize/2 pixels each direction
                        draw_rectangle((x + cellWidth // 2 - topDoorSize // 2), y, topDoorSize, topDoorWidth, RED)
                    if thisCell.state.south == True:
                        #draw_line(x+topExitSize, y + cellHeight-1, x + cellWidth-topExitSize, y + cellHeight-1, exitColor)
                        #draw_rectangle(x+topExitSize, y + cellHeight-2, cellWidth-topExitSize*2, 2, exitColor)
                        #draw the exit from the center of the south wall, reaching topExitSize/2 pixels each direction
                        draw_rectangle((x + cellWidth // 2 - topDoorSize // 2), y + cellHeight - topDoorWidth, topDoorSize, topDoorWidth, GREEN)
                    if thisCell.state.east == True:
                        #draw_line(x + cellWidth-1, y+sideExitSize, x + cellWidth-1, y + cellHeight-sideExitSize, exitColor)
                        #draw_rectangle(x + cellWidth-2, y+sideExitSize, 2, cellHeight-sideExitSize*2, exitColor)
                        #draw the exit from the center of the east wall, reaching sideExitSize/2 pixels each direction
                        draw_rectangle(x + cellWidth - sideDoorWidth, y + cellHeight // 2 - sideDoorSize // 2, sideDoorWidth, sideDoorSize, YELLOW)
                    if thisCell.state.west == True:
                        #draw_line(x+1, y+sideExitSize, x+1, y + cellHeight-sideExitSize, exitColor)
                        #draw_rectangle(x, y+sideExitSize, 2, cellHeight-sideExitSize*2, exitColor)
                        #draw the exit from the center of the west wall, reaching sideExitSize/2 pixels each direction
                        draw_rectangle(x, y + cellHeight // 2 - sideDoorSize // 2, sideDoorWidth, sideDoorSize, PURPLE)
                
