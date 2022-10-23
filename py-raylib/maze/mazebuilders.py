# various maze builder classes
# ported from C# version
import random
DEBUG_MAZE = False

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
        # try from top to bottom, left to right
        for row in range(self.level.height):
            # at start of each row, create a new "run" of cells in an array.
            run = []
            for col in range(self.level.width):
                cell = self.level.getCellAt(row, col)
                if DEBUG_MAZE: 
                    print("row: ", row, " col: ", col, " cell: ", cell)
                # add this cell to the run
                run.append(cell)
                # if it's time to close the run (because we're at a N or E boundary,
                # or if a random roll dictates to close this run now), then link
                # to the north if possible, finish the run, and start a new run.
                # else link this cell to the east.
                atEasternBoundary = (col == (self.level.width - 1))
                atNorthernBoundary = (row == 0) #(self.level.height - 1)) # top not bottom
                shouldCloseOut = atEasternBoundary or (not atNorthernBoundary and random.randint(0, 1) == 0)
                if shouldCloseOut:
                    # choose one of the cells in the run at random
                    member = random.choice(run)
                    # if it's not on the northern border, link to the north
                    if not atNorthernBoundary:
                        #north = self.level.getNeighbor(member, "north")
                        #north = self.level.getNeighbor(member, 0)
                        member = cell
                        if member.state.north != None:
                            member.state.link("north")
                            if member.text == None:
                                member.text = "N"
                            else:
                                member.text += "N"
                            if DEBUG_MAZE: 
                                print("linking north")
                        else:
                            if DEBUG_MAZE:
                                print("can't link north")
                    # clear the run
                    run = []
                else:
                    # link to the east
                    member = cell
                    if member.state.east != None:
                        member.state.link("east")
                        if member.text == None:
                            member.text = "E"
                        else:
                            member.text += "E"
                        if DEBUG_MAZE:
                            print("linking east")
                    else:
                        if DEBUG_MAZE:
                            print("Can't link east")


#### TEST ###
""""
public class BinaryTreeMazeBuilder: MazeBuilder
    {
        // build a maze from a Grid using the BinaryTree method
       
        public BinaryTreeMazeBuilder()
        {
        }

        public new void buildMaze(Grid grid)
        {

            int rows = grid.Rows;
            int cols = grid.Columns;
            // iterate over each cell
            // start at the bottom [rows-1,0] and move upwards
            for (int i = rows - 1; i >= 0; i--)
            {
                for (int j = 0; j < cols; j++)
                {
                    Cell c = grid.Cells[i, j];
                    processCell(c);
                }
            }
        }

        public void processCell(Cell c)
        {
            
            List<Cell> neighbors = new List<Cell>();
            if (c.North != null)
            {
                neighbors.Add(c.North);
            }
            if (c.East != null)
            {
                neighbors.Add(c.East);
            }
            // randomly link cell with north or east neighbor, if available
            
            int n = neighbors.Count();
            if (n == 0)
            {
                return;
            }
            // using a d20 roll, modulus the # of exits available, to pick exit carved.
            int roll = rand.Next(20);
            int index = roll % n; // pick one of the possible n or e exits
            Console.Write("("+roll+","+n+","+index+")");
            Cell neighbor = null;
            if (n > 0)
            {
                neighbor = neighbors.ElementAt(index);
            }
            if (neighbor != null)
            {
                c.link(neighbor);
            }
        }
    }
"""

# Testing - Binary Tree version of MazeBuilder
class BinaryTreeMazeBuilder(MazeBuilder):
    """ build a maze from a Grid using the BinaryTree method
    """
    def __init__(self, level):
        super().__init__(level)
        

    def build(self):
        """ build a maze from a level using the BinaryTree method
        """
        rows = self.level.height
        cols = self.level.width
        print("BT: rows =", rows, "cols =", cols)
        # iterate over each cell
        # start at the bottom [rows-1,0] and move upwards
        for i in range(rows - 1, -1, -1):
            for j in range(0, cols):
                c = self.level.getCellAt(i, j) #[i][j]
                if DEBUG_MAZE:
                    print("BT: about to process", c, "from", i, j)
                self.processCell(c)

    def processCell(self, c):
        """ 
        """
        row = c.row
        col = c.col
        if DEBUG_MAZE:
            print("BT: cell is: ", c)
            print("row: ", row, " col: ", col, " cell: ", c)

        
        neighbors = []
        if c.state.north != None:
            neighbors.append(c.state.northDest)
            #c.state.link("north")
            #print("could link N", end="")
        if c.state.east != None:
            neighbors.append(c.state.eastDest)
            #c.state.link("east")
            #print("could link E", end="")
        # randomly link cell with north or east neighbor, if available
        
        n = len(neighbors)
        if n == 0:
            return
        # using a d20 roll, modulus the # of exits available, to pick exit carved.
        roll = random.randint(0, 20)
        index = roll % n # pick one of the possible n or e exits
        #print(" >rollan: ({},{},->{})".format(roll, n, index), end="")
        neighbor = None
        if n > 0:
            neighbor = neighbors[index]
        assert neighbor != None, "neighbor is None"
        if neighbor != None:
            print(" >linking to", neighbor)
            #c.link(neighbor)
            # determine which neighbor we're linking to
            if neighbor.state.southDest == c:
                c.state.link("north")
                if c.text == None:
                    c.text = "N"
                else:
                    c.text += "N"
                if DEBUG_MAZE:
                    print("linking north")
            if neighbor.state.westDest == c:
                c.state.link("east")
                if c.text == None:
                    c.text = "E"
                else:
                    c.text +="E"
                if DEBUG_MAZE:
                    print("linking east")
