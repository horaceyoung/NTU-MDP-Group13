from settings import *
import pygame as pg
import map_generator as map

class Robot(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = robot_image
        self.direction = pg.math.Vector2((0, -1))
        self.velocity = 35

        self.spawn_point = 17 * map.Map.tile_length
        self.rect = (map.Map.tile_gap, self.spawn_point + map.Map.tile_gap) #position of the robot
        self.censors = []
        self.add_censor(0, -100, 50, 100)
        self.add_censor(60, -40, 20, 40)

    def add_censor(self, pos_X_offset, pos_Y_offset, height, width):
        self.censors.append(Censor(self, pos_X_offset, pos_Y_offset, height, width))

    def move_forward(self):
        print(self.rect)
        if self.rect[0] >= map.Map.arena_border_left:
            self.rect += self.direction * self.velocity


    def rotate(self, degree):
        self.image  = pg.transform.rotate(self.image, -degree)
        self.direction = self.direction.rotate(degree).normalize()


class Censor(pg.sprite.Sprite):
    def __init__(self, robot, pos_X_offset, pos_Y_offset, width, height):
        pg.sprite.Sprite.__init__(self)
        self.color = (255, 0, 0)

    def spawn_censor(self, screen):
        pass
