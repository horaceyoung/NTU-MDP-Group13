import pygame as pg

import configurations
import fastest_path
import map
import robot

pg.init()
screen = pg.display.set_mode((1024, 768))
pg.display.set_caption("MDP Arena Simulator")

player_robot = robot.Robot()
robot_group = pg.sprite.Group(player_robot)
arena_map = map.Map()
arena_map.generate_map('map_config_1.txt')
running = True

while running:
    screen.fill((0,0,0))

    # generate the map
    arena_map.cells_group.draw(screen)
    robot_group.draw(screen)
    player_robot.sensors.draw(screen)
    # map update
    arena_map.map_update()

    # controls
    for event in pg.event.get():
        # sensors update
        for sensor in player_robot.sensors:
            sensor.sense(arena_map)
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
