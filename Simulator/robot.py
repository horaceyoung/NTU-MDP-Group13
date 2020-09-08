from settings import *
import pygame as pg
import map_generator as map
import numpy

class Robot(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = robot_image
        self.direction = pg.math.Vector2(0, -1)
        self.velocity = 35

        self.spawn_point = 17 * map.Map.tile_length

        self.rect = self.image.get_rect()
        self.rect.x = map.Map.tile_gap
        self.rect.y = self.spawn_point + map.Map.tile_gap #position of the robot
        self.center = pg.math.Vector2(self.rect.x+50, self.rect.y+50)

        self.censors = pg.sprite.Group()
        self.add_censor(20, 40, 0, -50)
        self.add_censor(20, 40, 40, -50)
        self.add_censor(20, 40, -40, -50)

    def add_censor(self, width, height, center_x_offset, center_y_offset):
        self.censors.add(Censor(width, height, center_x_offset, center_y_offset, self))

    def is_in_arena(self, rect):
        if rect.x>= map.Map.arena_border_left and rect.x <= map.Map.arena_border_right and rect.y >= map.Map.arena_border_up and rect.y <= map.Map.arena_border_down:
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
            for censor in self.censors:
                censor.position_update(self)

    def rotate(self, degree):
        self.image  = pg.transform.rotate(self.image, -degree)
        self.direction = self.direction.rotate(degree).normalize()

        #update censors
        for censor in self.censors:
            censor.rotation_update(self, degree)





class Censor(pg.sprite.Sprite):
    def __init__(self, width, height, center_x_offset, center_y_offset, robot):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = robot.rect.center + pg.math.Vector2(center_x_offset, center_y_offset)
        self.color = (255, 0, 0)

        pg.draw.rect(self.image, self.color, pg.Rect(0, 0, width, height), 4)

    def rotation_update(self, robot, degree):
        center_diff_vec = pg.math.Vector2(tuple(numpy.subtract(self.rect.center, robot.rect.center)))
        rotated_center_diff_vec = center_diff_vec.rotate(degree)
        self.rect.center = robot.rect.center + rotated_center_diff_vec
        self.image = pg.transform.rotate(self.image, degree)

    def position_update(self, robot):
        self.rect.center += robot.velocity * robot.direction

    def collision_update(self, map):
        collided_tiles = pg.sprite.spritecollide(self, map.tiles_group, False)
        collided_tiles_with_distance = []
        for collided_tile in collided_tiles:
            collided_tiles_with_distance.append((collided_tile, pg.math.Vector2(self.rect.x, self.rect.y).distance_to(
                pg.math.Vector2(collided_tile.rect.x, collided_tile.rect.y))))

        #sort the tiles by the distance between its center and the center of the censor
        collided_tiles_with_distance.sort(key=lambda x:x[1])
        for collided_tile_tuple in collided_tiles_with_distance:
            map.map_tiles[collided_tile_tuple[0].row][collided_tile_tuple[0].col].discovered = True
            if collided_tile_tuple[0].is_obstacle:
                collided_tile_tuple[0].update_color((0, 0, 255))
                break


