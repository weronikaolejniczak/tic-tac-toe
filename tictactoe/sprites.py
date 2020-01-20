import pygame as pg
from tictactoe import settings


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, XorO):
        # call the parent class (Sprite) constructor
        super().__init__()
        self.WIDTH = settings.P_WIDTH
        self.HEIGHT = settings.P_HEIGHT
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.XorO = XorO
        self.image = pg.Surface([settings.WIDTH, settings.HEIGHT])
        self.image.fill(settings.WHITE)
        self.image.set_colorkey(settings.WHITE)

        # draw a red square
        # pg.draw.rect(self.image, settings.RED, [self.pos_x, self.pos_y, self.WIDTH, self.HEIGHT])

        # draw an X or O
        if XorO == "X" or XorO == "x":
            self.image = pg.image.load("resources/x.png").convert_alpha()
        elif XorO == "O" or XorO == "o":
            self.image = pg.image.load("resources/o.png").convert_alpha()

        # fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
