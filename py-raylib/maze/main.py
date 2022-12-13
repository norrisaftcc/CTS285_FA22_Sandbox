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
    screen_width = int(800 * 1.8)
    screen_height = int(450 * 1.8)
    
    COLS = 16
    ROWS = 9
    
    cellWidth = int(screen_width // COLS)
    cellHeight = int(screen_height // ROWS)

    init_window(screen_width, screen_height, "raylib [core] example - basic window")
    set_target_fps(60)               # Set our game to run at 60 frames-per-second
    
    # init
    # create a level to display
    level = MazeLevel(COLS, ROWS, cellWidth, cellHeight, BLACK, LIGHTGRAY) # border, background
   
    level.makeLevel(cellWidth, cellHeight)
    level.labelCells() # default labels are coordinates 
    #defaultLevel = copy.deepcopy(level) # this recurses forever, oops
    """
    # maze with sidewinder
    sidewinder = Sidewinder(level)
    sidewinder.build()
    """
    # BT
    btBuilder = BinaryTreeMazeBuilder(level)
    btBuilder.build()
    
    #init_window(800, 450, "Hello")
    # Draw
    while not window_should_close():
        # update - is key down is repeating, we only need to do these once per press
        # key bindings - R resets to blank level, S builds a new Sidewinder maze
        if is_key_down(KeyboardKey.KEY_R):
            print("reset")
            # create a level to display
            level = MazeLevel(COLS, ROWS, cellWidth, cellHeight, BLACK, LIGHTGRAY) # border, background
        
            level.makeLevel(cellWidth, cellHeight)
            level.labelCells() # default labels are coordinates 
            
        if is_key_down(KeyboardKey.KEY_S):
            # create a level to display
            level = MazeLevel(COLS, ROWS, cellWidth, cellHeight, BLACK, LIGHTGRAY) # border, background
        
            level.makeLevel(cellWidth, cellHeight)
            level.labelCells() # default labels are coordinates 
            # re-sidewider
            sidewinder = Sidewinder(level)
            sidewinder.build()
        if is_key_down(KeyboardKey.KEY_B):
            print("binary tree maze")
            level = MazeLevel(COLS, ROWS, cellWidth, cellHeight, BLACK, LIGHTGRAY) # border, background
        
            level.makeLevel(cellWidth, cellHeight)
            level.labelCells() # default labels are coordinates 
            # remaze as binary tree
            btBuilder = BinaryTreeMazeBuilder(level)
            btBuilder.build()
            
        # draw
        begin_drawing()
        clear_background(LIGHTGRAY)
        # draw cells
        level.draw()
        end_drawing()
    close_window()
    


if __name__ == "__main__":
    main()