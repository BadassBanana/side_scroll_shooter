import pygame as pg
from settings import *

class Tile(pg.sprite.Sprite):
    """The class definition for the tiles
        that make the backround."""
    def __init__(self, x = 33, y = 35, centerx = WIDTH / 2, centery = HEIGHT - 33):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((x, y))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center =(centerx, centery)

tile_list = pg.sprite.Group()

for i in range(16):
    tile = Tile(centerx = 0 + (33 * i))
    tile_list.add(tile)
