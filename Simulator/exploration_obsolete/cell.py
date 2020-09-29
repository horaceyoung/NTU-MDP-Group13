import configurations


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.isVirtualWall = False
        self.isExplored = False
        self.isObstacle = False
        self.isPath = False

    def setIsObstacle(self, value):
        self.isObstacle = value

    def setVirtualWall(self, value):
        if value:
            self.isVirtualWall = True
        else:
            if (
                self.row != 0
                and self.row != (configurations.MAP_ROWS - 1)
                and self.col != 0
                and self.col != (configurations.MAP_COLS - 1)
            ):
                self.isVirtualWall = false

    def setIsExplored(self, value):
        self.isExplored = value

    def getIsObstacle(self):
        if self.isObstacle == True:
            return 1
        else:
            return 0
