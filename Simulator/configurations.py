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
    ERROR = 'E'

class Direction(enum.Enum):
    LEFT = pg.Vector2(-1, 0)
    UP = pg.Vector2(0, -1)
    RIGHT = pg.Vector2(1, 0)
    DOWN = pg.Vector2(0, 1)

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
