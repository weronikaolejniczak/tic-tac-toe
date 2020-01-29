#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame as pg
from game import Game


def main():
    # create the game object
    game = Game()
    game.show_start_screen()

    while True:
        game.run()


if __name__ == '__main__':
    main()
    pg.quit()
