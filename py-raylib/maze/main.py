# sample raylib application

#testing
from __future__ import annotations
# import type checking
from typing import TYPE_CHECKING
# graphics
#import graphics as g
# raylib
from pyray import *

# data classes
from levels import *
from mazebuilders import *

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    #screen_width = 800
    #screen_height = 450
    screen_width = int(800 * 1.2)
    screen_height = int(450 * 1.2)
    
    COLS = 16
    ROWS = 9
    
    cellWidth = int(screen_width // COLS)
    cellHeight = int(screen_height // ROWS)

    init_window(screen_width, screen_height, "raylib [core] example - basic window")
    set_target_fps(60)               # Set our game to run at 60 frames-per-second
    
    #cells = cellInit(COLS, ROWS, cellWidth, cellHeight)
    # create a level to display
    level = MazeLevel(COLS, ROWS, cellWidth, cellHeight, BLACK, LIGHTGRAY) # border, background
   
    level.makeLevel(cellWidth, cellHeight)
    level.labelCells() # default labels are coordinates 
    
    # try linking two cells
    northCell = level.getCellAt(0, 0)
    southCell = level.getCellAt(1, 0)
    southCell.state.link("north") # bidi by default
    #northCell.state.link("south", False) # unidirectional
    eastCell = level.getCellAt(0, 1)
    eastCell.state.link("west") # bidi by default
    
    sidewinder = Sidewinder(level)
    sidewinder.build()
    
    #init_window(800, 450, "Hello")
    while not window_should_close():
        begin_drawing()
        clear_background(LIGHTGRAY)
        # draw cells
        level.draw()
        
        
        end_drawing()
    close_window()
    


if __name__ == "__main__":
    main()