import enum

class Movement(enum.Enum):
    LEFT = 'L'
    RIGHT = 'R'
    FORWARD = 'F'
    BACKWARD = 'B'
    CALIBRATE = 'C'
    ERROR = 'E'

class Direction(enum.Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

def directionPrint(dir):
    if(dir == Direction.NORTH):
        return 'N'
    elif(dir == Direction.EAST):
        return 'E'
    elif(dir == Direction.SOUTH):
        return 'S'
    elif(dir == Direction.WEST):
        return 'W'

def getNextDir(curDir):
    return Direction(((curDir.value+1)%4))

def getPrevDir(curDir):
    return Direction(((curDir.value+4-1)%4))


GOAL_ROW = 18                          # row no. of goal cell
GOAL_COL = 13                          # col no. of goal cell
START_ROW = 1                          # row no. of start cell
START_COL = 1                          # col no. of start cell
MOVE_COST = 10                         #cost of FORWARD, BACKWARD movement
TURN_COST = 20                         # cost of RIGHT, LEFT movement
SPEED = 100                            # delay between movements (ms)
START_DIR = Direction.NORTH      # start direction
SENSOR_SHORT_RANGE_L = 1               # range of short range sensor (cells)
SENSOR_SHORT_RANGE_H = 2               # range of short range sensor (cells)
SENSOR_LONG_RANGE_L = 3                # range of long range sensor (cells)
SENSOR_LONG_RANGE_H = 4                # range of long range sensor (cells)
INFINITE_COST = 9999


# Map Constants

MAP_SIZE = 300    # total num of cells
MAP_ROWS = 20     # total num of rows
MAP_COLS = 15     # total num of cols
GOAL_ROW = 18     # row no. of goal cell
GOAL_COL = 13
