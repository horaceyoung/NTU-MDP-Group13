import robot
import configurations
from Exploration import cell


class Map:

    # Map constructor
    # def __init__(self):
    def __init__(self, bot):
        self.bot = bot

        self.grid = []
        self.row = []
        for x in range(configurations.MAP_ROWS):
            for y in range(configurations.MAP_COLS):
                self.row.append(cell.Cell(x, y))
                if (
                    x == 0
                    or y == 0
                    or x == (configurations.MAP_ROWS - 1)
                    or y == (configurations.MAP_COLS - 1)
                ):
                    self.row[y].setVirtualWall(True)
            self.grid.append(self.row)
            self.row = []

    # Check whether column and row valid, return bool
    def checkValidCoordinates(self, row, col):
        return (
            row >= 0
            and col >= 0
            and row < configurations.MAP_ROWS
            and col < configurations.MAP_COLS
        )

    # Check whether row and column belongs to start zone, return bool
    def inStartZone(self, row, col):
        return row >= 0 and row <= 2 and col >= 0 and col <= 2

    # Check whether row and col are in goal zone, return bool
    def inGoalZone(self, row, col):
        return (
            row <= configurations.GOAL_ROW + 1
            and row >= configurations.GOAL_ROW - 1
            and col <= configurations.GOAL_COL + 1
            and col >= configurations.GOAL_COL - 1
        )

    # Get particular cell in grid Map, return object Cell
    def getCell(self, row, col):
        return self.grid[row][col]

    # Check if cell is an is an obstacle, return bool
    def isObstacleCell(self, row, col):
        return self.grid[row][col].isObstacle

    # Check if cell is a wall, return bool
    def isVirtualWallCell(self, row, col):
        return self.grid[row][col].isVirtualWall

    # sets all cells in grid to an explored state
    def setAllExplored(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                self.grid[x][y].setIsExplored(True)

    # set all cells in grid to unexplored state
    def setAllUnexplored(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                if self.inStartZone(x, y) or self.inGoalZone(x, y):
                    self.grid[x][y].setIsExplored(True)
                else:
                    self.grid[x][y].setIsExplored(False)

    # Set Cell object as obstacle
    def setObstacleCell(self, row, col, obstacle):
        if obstacle and (self.inStartZone(row, col) or self.inGoalZone(row, col)):
            return None

        self.grid[row][col].setIsObstacle(obstacle)

        if row >= 1:
            self.grid[row - 1][col].setVirtualWall(obstacle)  # bottom cell

            if col < configurations.MAP_COLS - 1:
                self.grid[row - 1][col + 1].setVirtualWall(
                    obstacle
                )  # bottom-right cell

            if col >= 1:
                self.grid[row - 1][col - 1].setVirtualWall(obstacle)  # bottom-left cell

        if row < configurations.MAP_ROWS - 1:
            self.grid[row + 1][col].setVirtualWall(obstacle)  # top cell

            if col < configurations.MapConstants.MAP_COLS - 1:
                self.grid[row + 1][col + 1].setVirtualWall(obstacle)  # top-right cell

            if col >= 1:
                self.grid[row + 1][col - 1].setVirtualWall(obstacle)  # top-left cell

        if col >= 1:
            self.grid[row][col - 1].setVirtualWall(obstacle)  # left cell

        if col < MapConstants.MAP_COLS - 1:
            self.grid[row][col + 1].setVirtualWall(obstacle)  # right cell

    # Check whether cell is an obstacle or wall
    def getIsObstacleOrWall(self, row, col):
        return (not self.checkValidCoordinates(row, col)) or self.getCell(
            row, col
        ).isObstacle

    def printVirtualMap(self):
        print_row = ""
        for x in range(configurations.MAP_ROWS):
            for y in range(configurations.MAP_COLS):
                # string = str(test_map.grid[x][y].row) + " "
                if self.grid[x][y].isPath:
                    string = "8 "
                elif self.grid[x][y].isExplored:
                    string = "1 "
                else:
                    string = "0 "
                print_row = print_row + string
            print(print_row)
            print_row = ""


# This section is for debug purpose
if __name__ == "__main__":
    test_bot = robot.RobotAlgo(
        configurations.START_ROW, configurations.START_COL, False
    )
    test_map = Map(test_bot)
    test_row = ""

    # Map Construction Test
    """
    for x in range(configurations.MAP_ROWS):
        for y in range(configurations.MAP_COLS):
            #string = str(test_map.grid[x][y].row) + " "
            string = str(test_map.grid[x][y].col) + " "
            test_row = test_row + string
        print(test_row)
        test_row = ""
    """
    # setVirtualWall Testing
    for x in range(configurations.MAP_ROWS):
        for y in range(configurations.MAP_COLS):
            # string = str(test_map.grid[x][y].row) + " "
            if test_map.grid[x][y].isVirtualWall:
                string = "1 "
            else:
                string = "0 "
            test_row = test_row + string
        print(test_row)
        test_row = ""
