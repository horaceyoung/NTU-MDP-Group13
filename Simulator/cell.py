import pygame as pg

class Cell(pg.sprite.Sprite):
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
        self.row = 0
        self.col = 0

        self.is_start_goal_zone = False
        self.is_obstacle = False
        self.discovered = False

    def update_color(self, color):
        self.color = color
        pg.draw.rect(self.image, self.color, pg.Rect(0,0, 35, 35))
