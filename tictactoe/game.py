import pygame as pg
from tictactoe import settings
from tictactoe.sprites import Player
import sys


# tilemap
textures = {
            X: pg.image.load("resources\\x.png"),
            O: pg.image.load("resources\\o.png")
            }

tilemap = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            ]


class Game:
    def __init__(self, width, height, fps):
        self.WIDTH = width
        self.HEIGHT = height
        self.FPS = fps
        self.size = (width, height)
        self.caption = "Tic-tac-toe"
        self.clock = pg.time.Clock()
        self.screen = self.create_window()
        self.run = True
        self.all_sprites_list = pg.sprite.Group()

    @staticmethod
    def initialize():
        pg.init()

    def create_window(self):
        screen = pg.display.set_mode(self.size)
        pg.display.set_caption(self.caption)

        return screen

    def draw_board(self):
        self.screen.fill(settings.WHITE)

        # draw vertical lines
        pg.draw.line(self.screen, settings.BLACK, [self.WIDTH / 3, 0], [self.WIDTH / 3, self.HEIGHT], 3)
        pg.draw.line(self.screen, settings.BLACK, [2 * self.WIDTH / 3, 0], [2 * self.WIDTH / 3, self.HEIGHT], 3)

        # draw horizontal lines
        pg.draw.line(self.screen, settings.BLACK, [0, self.HEIGHT / 3], [self.WIDTH, self.HEIGHT / 3], 3)
        pg.draw.line(self.screen, settings.BLACK, [0, 2 * self.HEIGHT / 3], [self.WIDTH, 2 * self.HEIGHT / 3], 3)

        # draw sprites
        self.all_sprites_list.draw(self.screen)

        # update the screen
        pg.display.flip()

        # limit to FPS frames per second
        self.clock.tick(self.FPS)

    def events(self):
        # main event loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
                sys.exit()

    def game_loop(self):
        # main program loop
        while self.run:
            self.events()
            self.all_sprites_list.update()
            self.draw_board()


g = Game(settings.WIDTH, settings.HEIGHT, settings.FPS)
player1 = Player(100, 100, "O")
player2 = Player(200, 200, "x")
g.all_sprites_list.add(player1)
g.initialize()
g.game_loop()
pg.quit()
