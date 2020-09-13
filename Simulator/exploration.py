import cell
import map
import configurations
import robot
import time
import fastestPath
#import commMgr

class Exploration:
    def __init__(self,exploredMap,realMap,bot,coverageLimit,timeLimit):
        self.exploredMap = exploredMap
        self.realMap = realMap
        self.bot = bot
        self.coverageLimit = coverageLimit
        self.timeLimit = timeLimit
        self.startTime = 0
        self.endTime = 0
        self.areaExplored = 0


    def runExploration(self):
        print("Starting Exploration...")
        self.startTime = time.time()
        self.endTime = self.startTime + self.timeLimit
        self.senseAndReload()
        self.areaExplored = self.calculateAreaExplored()  #Number of cells explored in grid
        print("Exploration Area: " + str(self.areaExplored))
        self.explorationLoop(self.bot.posRow,self.bot.posCol)


    def explorationLoop(self,r,c):
        while(True):
            self.nextMove()
            self.areaExplored = self.calculateAreaExplored()
            print("Area Explored: " + str(self.areaExplored))
            if(self.bot.posRow == r and self.bot.posCol == c):
                if(self.areaExplored >= 300):
                    break
            if(self.areaExplored >= self.coverageLimit or time.time() >= self.endTime):
                print("areaExplored, coverageLimit, curTime, endTime: ", self.areaExplored,self.coverageLimit,time.time(),self.endTime)
                break
        #path = fastestPath.astar(self.exploredMap, (self.bot.posRow,self.bot.posCol) , (configurations.START_ROW,configurations.START_COL))
        #fastestPath.runAStar(path,self.exploredMap)
        #self.goHome()


    def nextMove(self):
        if(self.lookRight()):
            self.moveBot(configurations.Movement.RIGHT)
            if(self.lookForward()):
                self.moveBot(configurations.Movement.FORWARD)
        elif(self.lookForward()):
            self.moveBot(configurations.Movement.FORWARD)
        elif(self.lookLeft()):
            self.moveBot(configurations.Movement.LEFT)
            if(self.lookForward()):
                self.moveBot(configurations.Movement.FORWARD)
        else:
            self.moveBot(configurations.Movement.RIGHT)
            self.moveBot(configurations.Movement.RIGHT)

    def lookRight(self):
        dir = self.bot.robotDir
        if(dir == configurations.Direction.NORTH):
            return self.eastFree()
        elif(dir == configurations.Direction.EAST):
            return self.southFree()
        elif(dir == configurations.Direction.SOUTH):
            return self.westFree()
        elif(dir == configurations.Direction.WEST):
            return self.northFree()
        else:
            return False

    def lookForward(self):
        dir = self.bot.robotDir
        if(dir == configurations.Direction.NORTH):
            return self.northFree()
        elif(dir == configurations.Direction.EAST):
            return self.eastFree()
        elif(dir == configurations.Direction.SOUTH):
            return self.southFree()
        elif(dir == configurations.Direction.WEST):
            return self.westFree()
        else:
            return False


    def lookLeft(self):
        dir = self.bot.robotDir
        if(dir == configurations.Direction.NORTH):
            return self.westFree()
        elif(dir == configurations.Direction.EAST):
            return self.northFree()
        elif(dir == configurations.Direction.SOUTH):
            return self.eastFree()
        elif(dir == configurations.Direction.WEST):
            return self.southFree()
        else:
            return False


    def northFree(self):
        botRow = self.bot.posRow
        botCol = self.bot.posCol
        return (self.isExploredNotObstacle(botRow+1,botCol-1) and self.isExploredAndFree(botRow+1, botCol) and self.isExploredNotObstacle(botRow+1,botCol+1))

    def eastFree(self):
        botRow = self.bot.posRow
        botCol = self.bot.posCol
        return (self.isExploredNotObstacle(botRow-1,botCol+1) and self.isExploredAndFree(botRow, botCol+1) and self.isExploredNotObstacle(botRow+1,botCol+1))

    def southFree(self):
        botRow = self.bot.posRow
        botCol = self.bot.posCol
        return (self.isExploredNotObstacle(botRow-1,botCol-1) and self.isExploredAndFree(botRow-1, botCol) and self.isExploredNotObstacle(botRow-1,botCol+1))

    def westFree(self):
        botRow = self.bot.posRow
        botCol = self.bot.posCol
        return (self.isExploredNotObstacle(botRow-1,botCol-1) and self.isExploredAndFree(botRow, botCol-1) and self.isExploredNotObstacle(botRow+1,botCol-1))

    """
    def goHome(self):
        if(not self.bot.touchedGoal and coverageLimit == 300 and timeLimit == 3600):
            goToGoal = FastestPathAlgo(self.exploredMap,self.bot,self.realMap)
            goToGoal.runFastestPath(configurations.GOAL_ROW, configurations.GOAL_COL)

        returnToStart = FastestPathAlgo(self.exploredMap,self.bot,self.realMap)
        returnToStart.runFastestPath(configurations.START_ROW, configurations.START_COL)

        print("Exploration Complete...")
        self.areaExplored = self.calculateAreaExplored()
        percentage = (self.areaExplored/300)*100
        print(percentage + "Coverage, "+ self.areaExplored + "Cells")
        print((int(time.time())-self.startTime) + "Seconds")
    """

    def isExploredNotObstacle(self,r,c):
        if(self.exploredMap.checkValidCoordinates(r,c)):
            tmp = self.exploredMap.getCell(r,c)
            return (tmp.isExplored and not tmp.isObstacle)
        return False

    def isExploredAndFree(self,r,c):
        if(self.exploredMap.checkValidCoordinates(r,c)):
            b = self.exploredMap.getCell(r,c)
            return (b.isExplored and not b.isVirtualWall and not b.isObstacle)
        return False

    def calculateAreaExplored(self):
        result = 0
        for x in range(configurations.MAP_ROWS):
            for y in range(configurations.MAP_COLS):
                if(self.exploredMap.getCell(x,y).isExplored):
                    result += 1
        return result


    def moveBot(self,m):
        self.bot.move(m)
        #self.exploredMap.reload()
        self.bot.setSensors()
        self.bot.sense(self.exploredMap,self.realMap)
        self.exploredMap.printVirtualMap()
        #self.senseAndReload()
        #INCOMPLETE: Still got missing part. Need to calibrate movement for REAL bot

    def senseAndReload(self):
        self.bot.setSensors()
        self.bot.sense(self.exploredMap,self.realMap)
        #self.exploredMap.reload()            # Need to update exploredMap after sensing


    def turnBotDirection(self,targetDir):
        numOfTurn = abs(self.bot.robotDir.value - targetDir.value)
        if(numOfTurn>2):
            numOfTurn = numOfTurn % 2

        if(numOfTurn == 1):
            if(configurations.getNextDir(self.bot.robotDir)==targetDir):
                self.moveBot(configurations.Movement.RIGHT)
            else:
                self.moveBot(configurations.Movement.LEFT)
        elif(numOfTurn == 2):
            self.moveBot(configurations.Movement.RIGHT)
            self.moveBot(configurations.Movement.RIGHT)


    #INCOMPLETE: STILL NEED HANDLE CALIBRATION FOR ROBOT
    """
    def canCalibrateOnTheSpot(self,botDir):
        row = self.bot.getRobotPosRow()
        col = self.bot.getRobotPosCol()
        if(botDir == configurations.Direction.NORTH):
            return self.exploredMap.getIsObstacleOrWall(row+2,col-1) and self.exploredMap.getIsObstacleOrWall(row+2,col) and self.exploredMap.getIsObstacleOrWall(row+2,col+1)
        elif(botDir == configurations.Direction.NORTH):
            return self.exploredMap.getIsObstacleOrWall(row+2,col-1) and self.exploredMap.getIsObstacleOrWall(row+2,col) and self.exploredMap.getIsObstacleOrWall(row+2,col+1)



    def getCalibrationDirection(self):

    def calibrateBot(self,targetDir):
    """
