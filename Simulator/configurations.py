import enum
import pygame as pg
import os

cwd = os.getcwd()

non_obstacle_tile_color = (255, 255, 255)

robot_image = pg.transform.scale(
    pg.image.load(cwd + "\\assets\\icons\\robot.png"), (100, 100)
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


DIRECTION_VALUE = {
    Direction.UP: 0,
    Direction.RIGHT: 1,
    Direction.DOWN: 2,
    Direction.LEFT: 3,
}

def convertY(y):
    col = abs((y-19))
    return col

def getNextDir(curDir):
    dir_val = DIRECTION_VALUE[curDir]
    dir_val = (dir_val + 1) % 4
    for direction, value in DIRECTION_VALUE.items():
        if value == dir_val:
            return direction


def getPrevDir(curDir):
    dir_val = DIRECTION_VALUE[curDir]
    dir_val = (dir_val + 4 - 1) % 4
    for direction, value in DIRECTION_VALUE.items():
        if value == dir_val:
            return direction


def getTurn(curDir, targetDir):
    if getNextDir(curDir) == targetDir:
        return 1
    elif getPrevDir(curDir) == targetDir:
        return -1
    else:
        return 2


def nextCellDir(cur, next):
    x1, y1 = cur[0], cur[1]
    x2, y2 = next[0], next[1]
    if x1 < x2:
        return Direction.RIGHT
    elif x1 > x2:
        return Direction.LEFT
    if y1 < y2:
        return Direction.UP
    elif y1 > y2:
        return Direction.DOWN


def sameDir(curDir, targetDir):
    if curDir == targetDir:
        return True
    else:
        return False

def rotateBackDefault(curDir):
    curIndex = DIRECTION_ARRAY.index(curDir)
    return 4 - curIndex

def getDirectionValue(curDir):
    dir = {(0,-1):0,
            (1,0):90,
            (0,1):180,
            (-1,0):270}
    return dir[(curDir[0],curDir[1])]

DIRECTION_ARRAY = [[0,-1],[1,0],[0,1],[-1,0]] #up,right,down,left
DEFAULT_DIR = (0,-1)  #Default direction
GOAL_ROW = 18  # row no. of goal cell
GOAL_COL = 13  # col no. of goal cell
START_ROW = 1  # row no. of start cell
START_COL = 1  # col no. of start cell
MOVE_COST = 10  # cost of FORWARD, BACKWARD movement
TURN_COST = 20  # cost of RIGHT, LEFT movement
SPEED = 100  # delay between movements (ms)
SENSOR_SHORT_RANGE_L = 1  # range of short range sensor (cells)
SENSOR_SHORT_RANGE_H = 2  # range of short range sensor (cells)
SENSOR_LONG_RANGE_L = 3  # range of long range sensor (cells)
SENSOR_LONG_RANGE_H = 4  # range of long range sensor (cells)
INFINITE_COST = 9999


# Map Constants

MAP_SIZE = 300  # total num of cells
MAP_ROWS = 20  # total num of rows
MAP_COLS = 15  # total num of cols
GOAL_ROW = 18  # row no. of goal cell
GOAL_COL = 13

if __name__ == "__main__":
    print(getPrevDir(Direction.UP))
    print(getNextDir(Direction.UP))
