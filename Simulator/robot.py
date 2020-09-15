import numpy
import pygame as pg
from map import Map
from sensor import Sensor
from configurations import *

class Robot(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = robot_image
        self.direction = pg.math.Vector2(0, -1)
        self.velocity = 35

        self.spawn_point = 17 * Map.cell_length

        self.rect = self.image.get_rect()
        self.rect.x = Map.cell_gap
        self.rect.y = self.spawn_point + Map.cell_gap #position of the robot

        self.sensors = pg.sprite.Group()
        self.initialize_sensors()


    def add_sensor(self, width, height, center_x_offset, center_y_offset, direction):
        self.sensors.add(Sensor(width, height, center_x_offset, center_y_offset, direction, self))

    def initialize_sensors(self):
        """
        Robot Sensor placement
                         ^   ^   ^
                      SR  SR  SR
         << SR [X] [X] [X]
            < LR [X] [X] [X] SR >
                       [X] [X] [X]
        """
        # up sensors
        self.add_sensor(20, Map.cell_length* 8, 0, -Map.cell_length* 5.5, Direction.UP)
        self.add_sensor(20, Map.cell_length* 8, 30, -Map.cell_length* 5.5, Direction.UP)
        self.add_sensor(20, Map.cell_length* 8, -30, -Map.cell_length* 5.5, Direction.UP)
        # left sensors
        self.add_sensor(Map.cell_length * 8, 20, -Map.cell_length * 5.5, - Map.cell_length * 1, Direction.LEFT)
        self.add_sensor(Map.cell_length * 15, 20, -Map.cell_length * 9, 0, Direction.LEFT) # long-range sensor
        # right sensors
        self.add_sensor(Map.cell_length * 8, 20, Map.cell_length * 5.5, - Map.cell_length * 1, Direction.RIGHT)

    def is_in_arena(self, rect):
        if rect.x>= Map.arena_border_left and rect.x <= Map.arena_border_right and rect.y >= Map.arena_border_up and rect.y <= Map.arena_border_down:
            return True
        else:
            return False

    def move_forward(self):
        # if the robot is within the arena
        _rect = pg.Rect(self.rect)
        _rect.x += self.direction[0] * self.velocity
        _rect.y += self.direction[1] * self.velocity

        if self.is_in_arena(_rect):
            self.rect.x += self.direction[0] * self.velocity
            self.rect.y += self.direction[1] * self.velocity
            # update center
            self.rect.center = pg.math.Vector2(self.rect.x+50, self.rect.y+50)
            for sensor in self.sensors:
                sensor.position_update(self)

    def rotate(self, degree):
        self.image  = pg.transform.rotate(self.image, -degree)
        self.direction = self.direction.rotate(degree).normalize()

        #update sensors
        for sensor in self.sensors:
            sensor.rotation_update(self, degree)