from settings import *

import pygame as pg
import map_generator
import robot

pg.init()
screen = pg.display.set_mode((1024, 768))
pg.display.set_caption("MDP Arena Simulator")

player_robot = robot.Robot()
robot_group = pg.sprite.Group(player_robot)
arena_map = map_generator.Map()
arena_map.generate_map('map_config_1.txt')
running = True

while running:
    screen.fill((0,0,0))

    # generate the map
    arena_map.tiles_group.draw(screen)
    robot_group.draw(screen)
    player_robot.censors.draw(screen)
    #censors update
    for censor in player_robot.censors:
        censor.collision_update(arena_map)
    # map update
    arena_map.map_update()

    # controls
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                player_robot.move_forward()
            if event.key == pg.K_a:
                player_robot.rotate(-90)
            if event.key == pg.K_d:
                player_robot.rotate(90)

    pg.display.update()

