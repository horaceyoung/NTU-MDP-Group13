import pygame as pg
import os

cwd = os.getcwd()

non_obstacle_tile_color = (255,255,255)


robot_image = pg.transform.scale(
    pg.image.load(cwd + "\\assets\icons\\robot.png"),
    (100, 100)
    )