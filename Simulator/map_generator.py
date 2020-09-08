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

    tiles_group = pg.sprite.Group() # the tiles sprite group
    map_tiles = [] # a 20 * 15  list holding tile objects

    def __init__(self):
        pass

    def generate_map(self, map_config):

        with open(map_config_path + map_config, 'r') as map_config:
            tile_x = 5
            tile_y = 5
            for row in range(1, 21):
                line = map_config.readline()
                tile_row = []
                for col in range (0, 15):
                    if line[col] == '0':
                        tile = Tile(tile_x, tile_y)
                    elif line[col] == '1':
                        tile = Tile(tile_x, tile_y)
                        tile.is_obstacle = True
                    elif line[col] =='2':
                        tile = Tile(tile_x, tile_y)
                        tile.update_color((255, 255, 0))
                        tile.is_start_goal_zone = True
                    tile.row = row-1
                    tile.col = col
                    tile_row.append(tile)
                    tile_x += tile.length + tile.gap
                self.map_tiles.append(tile_row)
                tile_x = 5
                tile_y = 5 + (tile.length + tile.gap) *  row

        for tile in self.map_tiles:
            self.tiles_group.add(tile)

    def map_update(self):
        for tile_row in self.map_tiles:
            for tile in tile_row:
                if tile.is_obstacle == False and tile.discovered ==True and tile.is_start_goal_zone == False:
                    self.tiles_group.remove(tile)


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
        self.row = None
        self.col = None
        self.is_start_goal_zone = False
        self.is_obstacle = False
        self.discovered = False

    def update_color(self, color):
        self.color = color
        pg.draw.rect(self.image, self.color, pg.Rect(0,0, 35, 35))

