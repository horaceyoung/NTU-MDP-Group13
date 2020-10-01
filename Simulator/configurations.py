# import enum
# import pygame as pg
# import os

# cwd = os.getcwd()

# non_obstacle_tile_color = (255, 255, 255)

# robot_image = pg.transform.scale(
#     pg.image.load(cwd + "\\assets\\icons\\robot.png"), (100, 100)
# )

# map_config_path = cwd + "\\assets\\map\\"


# class Movement(enum.Enum):
#     LEFT = "L"
#     RIGHT = "R"
#     FORWARD = "F"
#     BACKWARD = "B"
#     CALIBRATE = "C"
#     ERROR = "E"


# class Direction(enum.Enum):
#     LEFT = pg.Vector2(-1, 0)
#     UP = pg.Vector2(0, -1)
#     RIGHT = pg.Vector2(1, 0)
#     DOWN = pg.Vector2(0, 1)


# DIRECTION_VALUE = {
#     Direction.UP: 0,
#     Direction.RIGHT: 1,
#     Direction.DOWN: 2,
#     Direction.LEFT: 3,
# }


# def getNextDir(curDir):
#     dir_val = DIRECTION_VALUE[curDir]
#     dir_val = (dir_val + 1) % 4
#     for direction, value in DIRECTION_VALUE.items():
#         if value == dir_val:
#             return direction


# def getPrevDir(curDir):
#     dir_val = DIRECTION_VALUE[curDir]
#     dir_val = (dir_val + 4 - 1) % 4
#     for direction, value in DIRECTION_VALUE.items():
#         if value == dir_val:
#             return direction


# def getTurn(curDir, targetDir):
#     if getNextDir(curDir) == targetDir:
#         return 1
#     elif getPrevDir(curDir) == targetDir:
#         return -1
#     else:
#         return 2


# def nextCellDir(cur, next):
#     x1, y1 = cur[0], cur[1]
#     x2, y2 = next[0], next[1]
#     if x1 < x2:
#         return Direction.RIGHT
#     elif x1 > x2:
#         return Direction.LEFT
#     if y1 < y2:
#         return Direction.UP
#     elif y1 > y2:
#         return Direction.DOWN


# def sameDir(curDir, targetDir):
#     if curDir == targetDir:
#         return True
#     else:
#         return False


# GOAL_ROW = 18  # row no. of goal cell
# GOAL_COL = 13  # col no. of goal cell
# START_ROW = 1  # row no. of start cell
# START_COL = 1  # col no. of start cell
# MOVE_COST = 10  # cost of FORWARD, BACKWARD movement
# TURN_COST = 20  # cost of RIGHT, LEFT movement
# SPEED = 100  # delay between movements (ms)
# SENSOR_SHORT_RANGE_L = 1  # range of short range sensor (cells)
# SENSOR_SHORT_RANGE_H = 2  # range of short range sensor (cells)
# SENSOR_LONG_RANGE_L = 3  # range of long range sensor (cells)
# SENSOR_LONG_RANGE_H = 4  # range of long range sensor (cells)
# INFINITE_COST = 9999


# # Map Constants

# MAP_SIZE = 300  # total num of cells
# MAP_ROWS = 20  # total num of rows
# MAP_COLS = 15  # total num of cols
# GOAL_ROW = 18  # row no. of goal cell
# GOAL_COL = 13

# if __name__ == "__main__":
#     print(getPrevDir(Direction.UP))
#     print(getNextDir(Direction.UP))


import enum
import pygame as pg
import os

cwd = os.getcwd()

non_obstacle_tile_color = (255,255,255)

robot_image = pg.transform.scale(
    pg.image.load(cwd + "\\assets\\icons\\robot.png"),
    (100, 100)
    )

map_config_path = cwd + "\\assets\\map\\"

class Movement(enum.Enum):
    LEFT = 'L'
    RIGHT = 'R'
    FORWARD = 'F'
    BACKWARD = 'B'
    CALIBRATE = 'C'
    READ_SENSOR = 'O'

class Direction(enum.Enum):
    LEFT = pg.Vector2(-1, 0)
    UP = pg.Vector2(0, -1)
    RIGHT = pg.Vector2(1, 0)
    DOWN = pg.Vector2(0, 1)
<<<<<<< HEAD


DIRECTION_VALUE = {Direction.UP: 0, Direction.RIGHT: 1, Direction.DOWN: 2, Direction.LEFT:3}


def getNextDir(curDir):
    dir_val = DIRECTION_VALUE[curDir]
    dir_val = (dir_val+1)%4
    for direction, value in DIRECTION_VALUE.items():
        if(value == dir_val):
            return direction

def getPrevDir(curDir):
    dir_val = DIRECTION_VALUE[curDir]
    dir_val = (dir_val+4-1)%4
    for direction, value in DIRECTION_VALUE.items():
        if(value == dir_val):
            return direction


def getTurn(curDir,targetDir):
    if(getNextDir(curDir)==targetDir):
=======
'''
def getDirectionValue(dir):
    if(dir == Direction.UP):
>>>>>>> parent of 2a46d71... Update
        return 1
    elif(dir == Direction.RIGHT):
        return 2
    elif(dir == Direction.DOWN):
        return 3
    elif(dir == Direction.LEFT):
        return 4

def getTurnCounter(curDir,targetDir):
    curDirVal = getDirectionValue(curDir)
    targetDirVal = getDirectionValue(targetDir)
    if((targetDirVal - curDirVal) > 2):
        turncounter = -1
    if((targetDirVal - curDirVal) < 0)
        turncounter = -1

def getNextDir(curDir):
    return Direction(((curDir.value+1)%4))

def getPrevDir(curDir):
    return Direction(((curDir.value+4-1)%4))

<<<<<<< HEAD
def rotateBackDefault(curDir):
    curIndex = DIRECTION_ARRAY.index(curDir)
    return 4 - curIndex 


DIRECTION_ARRAY = [[0,-1],[1,0],[0,1],[-1,0]]
DEFAULT_DIR = (0,-1)             # Default direction
=======
'''    
>>>>>>> parent of 2a46d71... Update
GOAL_ROW = 18                          # row no. of goal cell
GOAL_COL = 13                          # col no. of goal cell
START_ROW = 1                          # row no. of start cell
START_COL = 1                          # col no. of start cell
MOVE_COST = 10                         #cost of FORWARD, BACKWARD movement
TURN_COST = 20                         # cost of RIGHT, LEFT movement
SPEED = 100                            # delay between movements (ms)
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
<<<<<<< HEAD

if __name__ == '__main__':
    print(getPrevDir(Direction.UP))
    print(getNextDir(Direction.UP))
=======
>>>>>>> parent of 2a46d71... Update
