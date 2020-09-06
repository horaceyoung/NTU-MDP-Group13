from settings import *
import pygame as pg

class Map:
    # static variables
    height = 20
    width = 15
    config = 0

    non_obstacle_tile_width = 30 # with of the tile
    tile_length = 35  # tile_length - tile_width = the gap between tile gaps, alter here to adjust length
    tile_gap = tile_length - non_obstacle_tile_width
    arena_border_left = 5
    arena_border_up = 5
    arena_border_right = tile_length * 12
    arena_border_down = tile_length * 17

    def __init__(self):
        pass

    def generate_map(self, screen):

        tile_pos_x = tile_pos_y= self.tile_gap

        for horizontal in range(0, self.height):
            for vertical in range(0, self.width):
                pg.draw.rect(screen, non_obstacle_tile_color, (tile_pos_x, tile_pos_y,
                                                               self.non_obstacle_tile_width, self.non_obstacle_tile_width), 0)
                tile_pos_x += self.tile_length
            tile_pos_x = self.tile_gap
            tile_pos_y +=self.tile_length
