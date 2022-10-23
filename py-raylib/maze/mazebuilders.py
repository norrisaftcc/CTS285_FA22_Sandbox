# various maze builder classes
# ported from C# version
import random

class MazeBuilder:
    def __init__(self, level):
        self.level = level
        self.cellWidth = level.cellWidth
        self.cellHeight = level.cellHeight
        self.cellCount = len(self.level.cells)
        self.visited = []
        self.stack = []
        random.seed = 0 # seed random number generator, test with zero
        

    def build(self):
        # override this
        pass

    def getUnvisitedNeighbors(self, cell):
        # get neighbors
        neighbors = self.level.getNeighbors(cell)
        # filter out visited cells
        unvisited = []
        for cell in neighbors:
            if not cell.state.visited:
                unvisited.append(cell)
        return unvisited

    def randomNeighbor(self, cell):
        # get neighbors
        neighbors = self.level.getNeighbors(cell)
        # filter out visited cells
        unvisited = []
        for cell in neighbors:
            if not cell.state.visited:
                unvisited.append(cell)
        # pick one at random
        if len(unvisited) > 0:
            # return random.choice(unvisited)
            return unvisited[0]
        else:
            return None

    def randomCell(self):
        return random.choice(self.level.cells)

    def clearVisited(self):
        for cell in self.level.cells:
            cell.state.visited = False

    def clearStack(self):
        self.stack = []

    def clear(self):
        self.clearVisited()
        self.clearStack()

    def getVisitedCount(self):
        count = 0
        for cell in self.level.cells:
            if cell.state.visited:
                count += 1
        return count

    def getUnvisitedCount(self):
        count = 0
        for cell in self.level.cells:
            if not cell.state.visited:
                count += 1
        return count

    def getCellCount(self):
        return len(self.level.cells)

    def isDone(self):
        return (self.getVisitedCount() == self.getCellCount())
    
    
# Sidewinder -- probably the simplest
        """_
        // general algorithm:
        //
        // iterate through the grid, row by row.
        // at start of each row, create a new "run" of cells in an array.
        // if it's time to close the run (because we're at a N or E boundary,
        // or if a random roll dictates to close this run now), then link
        // to the north if possible, finish the run, and start a new run. 
        // else link this cell to the east.
        """
class Sidewinder(MazeBuilder):
    def __init__(self, level):
        super().__init__(level)

    def build(self):
        # iterate through the grid, row by row.
        # TODO: this code is jacked, but it does ... something
        # step through carefully
        # /TODO
        for row in range(self.level.height-1, 0, -1):
            # at start of each row, create a new "run" of cells in an array.
            run = []
            for col in range(self.level.width-1):
                cell = self.level.getCellAt(row, col)
                print("row: ", row, " col: ", col, " cell: ", cell)
                # add this cell to the run
                run.append(cell)
                # if it's time to close the run (because we're at a N or E boundary,
                # or if a random roll dictates to close this run now), then link
                # to the north if possible, finish the run, and start a new run.
                # else link this cell to the east.
                atEasternBoundary = (col == (self.level.width - 1))
                atNorthernBoundary = (row == (self.level.height - 1))
                shouldCloseOut = atEasternBoundary or (not atNorthernBoundary and random.randint(0, 1) == 0)
                if shouldCloseOut:
                    # choose one of the cells in the run at random
                    member = random.choice(run)
                    # if it's not on the northern border, link to the north
                    if not atNorthernBoundary:
                        #north = self.level.getNeighbor(member, "north")
                        #north = self.level.getNeighbor(member, 0)
                        member = cell
                        member.state.link("north")
                        print("linking north")
                    # clear the run
                    run = []
                else:
                    # link to the east
                    member = cell
                    member.state.link("east")
                    print("linking east")