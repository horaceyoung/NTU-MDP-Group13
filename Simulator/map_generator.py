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
    arena_border_right = tile_length * 13
    arena_border_down = tile_length * 18

    tiles = pg.sprite.Group()

    def __init__(self):
        pass

    def generate_map(self):
        tile_x = 5
        tile_y = 5

        for row in range (1, 21):
            for col in range (0, 15):
                tile = Tile(tile_x, tile_y)
                self.tiles.add(tile)
                tile_x += tile.length + tile.gap
            tile_x = 5
            tile_y = 5 + (tile.length + tile.gap) *  row

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.length = 30
        self.gap = 5
        self.color = (255, 255, 255)
        self.image = pg.Surface((self.length, self.length))
        self.rect = self.image.get_rect()
        pg.draw.rect(self.image, self.color, self.rect)
        self.rect.x = x
        self.rect.y = y