import pygame as pg
import fastest_path
import exploration
import map
import robot
from configurations import *

pg.init()
screen = pg.display.set_mode((1024, 768))
pg.display.set_caption("MDP Arena Simulator")
clock = pg.time.Clock()
player_robot = robot.Robot()
robot_group = pg.sprite.Group(player_robot)
arena_map = map.Map()
arena_map.generate_map('map_config_1.txt')
# an unresolved issue
arena_map.map_cells[18][3].discovered=True
arena_map.map_cells[19][3].discovered=True
running = True

while running:
    # controls
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                exploration.Exploration.next_move(player_robot, arena_map)
            if event.key == pg.K_a:
                player_robot.rotate(-90)
            if event.key == pg.K_d:
                player_robot.rotate(90)

    for sensor in player_robot.sensors:
        sensor.sense(arena_map, player_robot)
    exploration.Exploration.next_move(player_robot, arena_map)
    screen.fill((0, 0, 0))
    # generate the map
    arena_map.cells_group.draw(screen)
    robot_group.draw(screen)
    player_robot.sensors.draw(screen)
    # map update
    arena_map.map_update()

    clock.tick(10)


    pg.display.update()
