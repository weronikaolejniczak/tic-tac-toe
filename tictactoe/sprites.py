import pygame as pg
import minimax

import random


class Player(pg.sprite.Sprite):
    def __init__(self, game, ID):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.TILESIZE = (game.WIDTH/3, game.HEIGHT/3)
        self.TILEMAP = game.TILEMAP
        self.image = pg.Surface(self.TILESIZE)
        self.rect = (-200, -200)
        self.id = ID
        self.turns = 0
        self.x, self.y = (0, 0)

    def AI_turn(self):
        # TODO implement mini-max algorithm
        # X (2) -> AI
        x = random.randint(0, 2)
        y = random.randint(0, 2)

        if self.TILEMAP[x][y] == 0:
            self.TILEMAP[x][y] = 2
            self.turns += 1
            self.game.turn = "human"  # change the turn
            self.game.is_human_turn = True
        else:
            if not self.game.is_filled():
                self.AI_turn()
            else:
                self.game.draw()

                print("Board filled!")
                self.game.check_for_win(self.id, 2)

                pg.time.wait(2000)

                self.game.playing = False

    def determine_tile(self):
        x = self.x
        y = self.y
        index_x = 0
        index_y = 0

        # first row
        # TILEMAP[0][0] (x: 0-200 & y: 0-200) first column
        if (x in range(200)) and (y in range(200)):
            index_x, index_y = (0, 0)
        # TILEMAP[0][1] (x: 200-400 & y: 0-200) second column
        elif (x in range(200, 400)) and (y in range(200)):
            index_x, index_y = (0, 1)
        # TILEMAP[0][2] (x: 400-600 & y: 0-200) third column
        elif (x in range(400, 600)) and (y in range(200)):
            index_x, index_y = (0, 2)
        ###
        # second row
        # TILEMAP[1][0] (x: 0-200 & y: 200-400) first column
        elif (x in range(200)) and (y in range(200, 400)):
            index_x, index_y = (1, 0)
        # TILEMAP[1][1] (x: 200-400 & y: 200-400) second column
        elif (x in range(200, 400)) and (y in range(200, 400)):
            index_x, index_y = (1, 1)
        # TILEMAP[1][2] (x: 400-600 & y: 200-400) third column
        elif (x in range(400, 600)) and (y in range(200, 400)):
            index_x, index_y = (1, 2)
        ###
        # third row
        # TILEMAP[2][0] (x: 0-200 & y: 400-600) first column
        elif (x in range(200)) and (y in range(400, 600)):
            index_x, index_y = (2, 0)
        # TILEMAP[2][1] (x: 200-400 & y: 400-600) second column
        elif (x in range(200, 400)) and (y in range(400, 600)):
            index_x, index_y = (2, 1)
        # TILEMAP[2][2] (x: 400-600 & y: 400-600) third column
        elif (x in range(400, 600)) and (y in range(400, 600)):
            index_x, index_y = (2, 2)

        return index_x, index_y

    def human_turn(self):
        # O (1) -> human
        if pg.mouse.get_pressed()[0] == 1:
            self.x, self.y = pg.mouse.get_pos()
            index = self.determine_tile()

            if self.TILEMAP[index[0]][index[1]] == 0:
                self.TILEMAP[index[0]][index[1]] = 1
                self.turns += 1
                self.game.turn = "AI"  # change the turn
                self.game.is_human_turn = False

                if self.game.is_filled():
                    self.game.draw()

                    print("Board filled!")
                    self.game.check_for_win(self.id, 1)

                    pg.time.wait(2000)
                    self.game.playing = False

    def update(self):
        if self.game.is_human_turn:
            self.human_turn()
        else:
            self.AI_turn()
