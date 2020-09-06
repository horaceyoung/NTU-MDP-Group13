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
arena_map.generate_map()
for tile in arena_map.tiles.sprites():
    print(tile.rect.x, tile.rect.y)

running = True

while running:
    screen.fill((0,0,0))

    # generate the map
    arena_map.tiles.draw(screen)
    robot_group.draw(screen)
    player_robot.censors.draw(screen)
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
    pg.sprite.groupcollide(player_robot.censors, arena_map.tiles, False, True)
    pg.display.update()

