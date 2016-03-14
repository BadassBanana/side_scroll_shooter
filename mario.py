import pygame as pg
from tile import tile_list
from settings import *

class Mario(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()

        self.speedx = 0
        self.speedy = 0
        self.gravity = 0

        self.direction = "right"

        self.tile_list = tile_list

    def update(self):
        """Updates the player class so that it
        can move for every frame and also react
        to the gravity functions."""
        self.calc_grav()
        self.check_tiles()
        self.speedx = 0

        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx = -5
            self.direction = "left"

        if keystate[pg.K_RIGHT]:
            self.speedx = 5
            self.direction = "right"

        if keystate[pg.K_SPACE]:
            self.shoot()

        if keystate[pg.K_UP]:
            self.jump()

        if keystate[pg.K_s]:
            print str(self.speedy)

        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def calc_grav(self):
        """Calculates the effect of gravity"""
        tile_hit_list = pg.sprite.spritecollide(self, self.tile_list, False)
        if self.speedy == 0 and len(tile_hit_list) == 0:
            self.speedy = 1
        else:
            self.speedy += .35

        # Checks if player is on ground
        for tile in tile_hit_list:
            if self.rect.bottom > tile.rect.top:
                self.rect.bottom = tile.rect.top
                self.speedy = 0

    def jump(self):
        """Called whenever the sprite jumps"""
        self.rect.y += 2
        tile_hit_list = pg.sprite.spritecollide(self, self.tile_list, False)
        self.rect.y -= 2

        # Set our speed upwards if it is ok to jump
        if len(tile_hit_list) > 0:
            self.speedy = -10

    def shoot(self):
        """Called whenever SPACE is pressed
            so that the sprite shoots, obviously.
            """
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            player_bullets.add(bullet)

    def check_tiles(self):
        """Used to check if the player has
        collided with any tiles, that are
        used as floors"""
        tile_hit_list = pg.sprite.spritecollide(self, self.tile_list, False)
        for tile in tile_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.speedx > 0:
                self.rect.right = tile.rect.left
            elif self.speedx < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = tile.rect.right

mario = Mario()
player_bullets = pg.sprite.Group()

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 0
        self.speedy = 0

        if mario.direction == "left":
            self.speedx = -15

        if mario.direction == "right":
            self.speedx = 15


    def update(self):
        self.rect.x += self.speedx
        # kill if it moves off the screen
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

