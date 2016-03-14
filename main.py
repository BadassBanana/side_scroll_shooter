import pygame as pg
from settings import *
from mario import *
from tile import *
import sys

pg.init()

class States(object):
    """Defines all the states needed for the game
    Next and previous moves the game state forward
    and backwards whilst done and quit are there for
    quitting the gameloop or state."""
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None


class Menu(States):
    """The class for the menu and it inherits
    from states. It includes a cleanup and startup
    functions, and also the functions normally seen
    in a game loop such as update and draw."""
    def __init__(self):
        States.__init__(self)
        self.next = 'game'

    def cleanup(self):
        """Cleans up anything from the menu state
        that the game state shouldn't have
        when changing."""
        print('cleaning up Menu state stuff')

    def startup(self):
        """Just initialises variables and music
        needed for the menu state."""
        print('starting Menu state stuff')


    def get_event(self, event):
        """Gets the events taken during the menu
        state."""
        if event.type == pg.KEYDOWN:
            print('Menu State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, screen, dt):
        """Update section of the loop"""
        self.draw(screen)

    def draw(self, screen):
        """Draw section of the loop"""
        screen.fill((RED))

class Game(States):
    """Like the menu state except this would probably be used
    a lot more, as it is the gameloop."""
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'

    def cleanup(self):
       print('cleaning up Game state stuff')

    def startup(self):
        """This is where the all of the spritelists
        are spawned. The all_sprites group is made here.
        Any other sprite groups are made in their own files."""
        print('starting Game state stuff')
        self.all_sprites = pg.sprite.Group()
        self.player_bullets = player_bullets
        self.tile_list = tile_list
        self.all_sprites.add(mario)

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
            mario.kill()

    def update(self, screen, dt):
        self.draw(screen)

        self.all_sprites.update()
        self.tile_list.update()
        self.player_bullets.update()


    def draw(self, screen):
        screen.fill((BLUE))
        self.all_sprites.draw(screen)
        self.tile_list.draw(screen)
        self.player_bullets.draw(screen)

class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    def flip_state(self):
        self.state.done = False
        previous,self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous
    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
           self.flip_state()
        self.state.update(self.screen, dt)
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            pg.display.update()


if __name__ == '__main__':
    settings = {
        'fps' :FPS
    }

    app = Control(**settings)
    state_dict = {
        'menu': Menu(),
        'game': Game()
    }
    app.setup_states(state_dict, 'menu')
    app.main_game_loop()
    pg.quit()
    sys.exit()