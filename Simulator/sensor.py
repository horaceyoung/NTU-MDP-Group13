import pygame as pg
import numpy

class Sensor(pg.sprite.Sprite):
    def __init__(self, width, height, center_x_offset, center_y_offset, direction, robot):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = robot.rect.center + pg.math.Vector2(center_x_offset, center_y_offset)
        self.color = (255, 0, 0)
        self.border_width = 10
        self.direction = direction

        pg.draw.rect(self.image, self.color, pg.Rect(0, 0, width, height), self.border_width)

    def rotation_update(self, robot, degree):
        center_diff_vec = pg.math.Vector2(tuple(numpy.subtract(self.rect.center, robot.rect.center)))
        rotated_center_diff_vec = center_diff_vec.rotate(degree)
        self.image = pg.transform.rotate(self.image, degree)
        self.rect = self.image.get_rect(center=robot.rect.center + rotated_center_diff_vec)
        # robot.rect.center + rotated_center_diff_vec


    def position_update(self, robot):
        self.rect.center += robot.velocity * robot.direction

    def collision_update(self, map):
        collided_cells = pg.sprite.spritecollide(self, map.cells_group, False)
        collided_cells_with_distance = []
        for collided_cell in collided_cells:
            collided_cells_with_distance.append((collided_cell, pg.math.Vector2(self.rect.x, self.rect.y).distance_to(
                pg.math.Vector2(collided_cell.rect.x, collided_cell.rect.y))))

        #sort the cells by the distance between its center and the center of the sensor
        collided_cells_with_distance.sort(key=lambda x:x[1])
        for collided_cell_tuple in collided_cells_with_distance:
            map.map_cells[collided_cell_tuple[0].row][collided_cell_tuple[0].col].discovered = True
            if collided_cell_tuple[0].is_obstacle:
                collided_cell_tuple[0].update_color((0, 0, 255))
                break