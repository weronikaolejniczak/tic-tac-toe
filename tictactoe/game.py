import sys
import pygame as pg
import settings
from sprites import Player

O = pg.image.load(settings.O)
X = pg.image.load(settings.X)
END = pg.image.load(settings.END)
START = pg.image.load(settings.START)
BUTTON = pg.image.load(settings.BUTTON)
favicon = pg.image.load(settings.FAV)


class Game:
    def __init__(self):
        pg.init()  # initialize pygame module
        pg.font.init()
        print("Tic-tac-toe Mini-max algorithm project @ werolejniczak.github.com")
        self.font = pg.font.Font("resources/fonts/{}".format(settings.FONT), 50)
        self.WIDTH = settings.WIDTH
        self.HEIGHT = settings.HEIGHT
        self.size = (self.WIDTH, self.HEIGHT)
        self.TILEMAP = [[0 for x in range(3)] for y in range(3)]
        self.screen = pg.display.set_mode(self.size)  # create an instance of the pygame.Surface class
        pg.display.set_icon(favicon)
        pg.display.set_caption("Tic-tac-toe")  # set the caption of our window
        self.clock = pg.time.Clock()  # create an instance of Clock class
        self.FPS = settings.FPS
        self.start_time = 0
        self.end_time = 0
        self.all_sprites = pg.sprite.Group()
        self.playing = True
        self.dt = 0
        self.turn = "human"
        self.human = Player(self, "human")
        self.AI = Player(self, "AI")
        self.is_human_turn = True
        self.winner = ""
        self.start = None
        self.end = None
        self.orientation = ""

    def run(self):
        # game loop - set self.playing = False to end the game
        while self.playing:
            self.dt = self.clock.tick(self.FPS)
            self.events()
            self.update(self.turn)
            self.draw()

        self.show_go_screen()

    @staticmethod
    def quit():

        pg.quit()
        sys.exit()

    def check_for_win(self, player_id, integer):
        # win in a row
        for row in range(3):
            if self.TILEMAP[row][0] == self.TILEMAP[row][1] == self.TILEMAP[row][2] == integer:
                self.start = self.get_pos_from_index(row, 0)
                self.end = self.get_pos_from_index(row, 2)
                self.orientation = "horizontal"
                self.draw()

                # set the winner
                self.winner = player_id

        # win in a column
        for col in range(3):
            if self.TILEMAP[0][col] == self.TILEMAP[1][col] == self.TILEMAP[2][col] == integer:
                self.start = self.get_pos_from_index(0, col)
                self.end = self.get_pos_from_index(2, col)
                self.orientation = "vertical"
                self.draw()

                # set the winner
                self.winner = player_id

        # win diagonally
        if self.TILEMAP[0][0] == self.TILEMAP[1][1] == self.TILEMAP[2][2] == integer:
            self.start = self.get_pos_from_index(0, 0)
            self.end = self.get_pos_from_index(2, 2)
            self.orientation = "anti-diagonal"
            self.draw()

            # set the winner
            self.winner = player_id

        if self.TILEMAP[0][2] == self.TILEMAP[1][1] == self.TILEMAP[2][0] == integer:
            self.start = self.get_pos_from_index(0, 2)
            self.end = self.get_pos_from_index(2, 0)
            self.orientation = "diagonal"
            self.draw()

            # set the winner
            self.winner = player_id

        if self.is_filled() and self.winner == "":
            # set the winner
            self.winner = "draw"

    def is_filled(self):
        boolean = True

        for i in range(3):
            for j in range(3):
                if self.TILEMAP[i][j] == 0:
                    boolean = False

        return boolean

    def update(self, current_turn):
        # update portion of the game loop
        if current_turn == "human":
            self.human.update()
            self.check_for_win(self.human.id, 1)

            if self.winner == "human":
                self.playing = False

        elif current_turn == "AI":
            self.AI.update()
            self.check_for_win(self.AI.id, 2)

            if self.winner == "AI":
                self.playing = False

    @staticmethod
    def get_pos_from_index(x, y):
        pos_x = 0
        pos_y = 0

        # first row
        # TILEMAP[0][0] (x: 0-200 & y: 0-200) first column
        if x == 0 and y == 0:
            pos_x, pos_y = (0, 0)
        # TILEMAP[0][1] (x: 200-400 & y: 0-200) second column
        elif x == 0 and y == 1:
            pos_x, pos_y = (200, 0)
        # TILEMAP[0][2] (x: 400-600 & y: 0-200) third column
        elif x == 0 and y == 2:
            pos_x, pos_y = (400, 0)
        ###
        # second row
        # TILEMAP[1][0] (x: 0-200 & y: 200-400) first column
        elif x == 1 and y == 0:
            pos_x, pos_y = (0, 200)
        # TILEMAP[1][1] (x: 200-400 & y: 200-400) second column
        elif x == 1 and y == 1:
            pos_x, pos_y = (200, 200)
        # TILEMAP[1][2] (x: 400-600 & y: 200-400) third column
        elif x == 1 and y == 2:
            pos_x, pos_y = (400, 200)
        ###
        # third row
        # TILEMAP[2][0] (x: 0-200 & y: 400-600) first column
        elif x == 2 and y == 0:
            pos_x, pos_y = (0, 400)
        # TILEMAP[2][1] (x: 200-400 & y: 400-600) second column
        elif x == 2 and y == 1:
            pos_x, pos_y = (200, 400)
        # TILEMAP[2][2] (x: 400-600 & y: 400-600) third column
        elif x == 2 and y == 2:
            pos_x, pos_y = (400, 400)

        pos = (pos_x, pos_y)

        return pos

    def draw_winning_line(self, orientation):
        # horizontal lines
        if orientation == "horizontal":
            pg.draw.line(self.screen, settings.BLACK,
                         [self.start[0] + 50, self.start[1] + 100],
                         [self.end[0] + 150, self.end[1] + 100],
                         4)

        # vertical lines
        elif orientation == "vertical":
            pg.draw.line(self.screen, settings.BLACK,
                         [self.start[0] + 100, self.start[1] + 50],
                         [self.end[0] + 100, self.end[1] + 150],
                         4)

        # anti-diagonal: T[0][0] -> T[2][2]
        elif orientation == "anti-diagonal":
            pg.draw.line(self.screen, settings.BLACK,
                         [self.start[0] + 100, self.start[1] + 100],
                         [self.end[0] + 100, self.end[1] + 100],
                         4)

        # diagonal: T[2][0] -> T[2][2]
        elif orientation == "diagonal":
            pg.draw.line(self.screen, settings.BLACK,
                         [self.start[0] + 100, self.start[1] + 100],
                         [self.end[0] + 100, self.end[1] + 100],
                         4)

    def draw_tilemap(self):
        for i in range(3):
            for j in range(3):
                if self.TILEMAP[i][j] == 1:
                    # draw O (human) in correct position
                    self.screen.blit(O, self.get_pos_from_index(i, j))
                elif self.TILEMAP[i][j] == 2:
                    # draw X (AI) in correct position
                    self.screen.blit(X, self.get_pos_from_index(i, j))

    def draw_grid(self):
        # draw vertical lines
        pg.draw.line(self.screen, settings.LINES,
                     [self.WIDTH / 3, 0],
                     [self.WIDTH / 3, self.HEIGHT],
                     3)

        pg.draw.line(self.screen, settings.LINES,
                     [2 * self.WIDTH / 3, 0],
                     [2 * self.WIDTH / 3, self.HEIGHT],
                     3)

        # draw horizontal lines
        pg.draw.line(self.screen, settings.LINES,
                     [0, self.HEIGHT / 3],
                     [self.WIDTH, self.HEIGHT / 3],
                     3)

        pg.draw.line(self.screen, settings.LINES,
                     [0, 2 * self.HEIGHT / 3],
                     [self.WIDTH, 2 * self.HEIGHT / 3],
                     3)

    def draw(self):
        self.screen.fill(settings.BOARD)

        # draw the grid lines
        self.draw_grid()

        # draw the tilemap
        self.draw_tilemap()

        # draw sprites
        self.all_sprites.draw(self.screen)

        # draw winning lines (if there's a win)
        if self.start is not None and self.end is not None and self.orientation != "":
            self.draw_winning_line(self.orientation)

        # update the screen
        pg.display.flip()

    def events(self):
        # main event loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == 27: # press ESCAPE to quit
                    self.playing = False
                    self.quit()

    def show_start_screen(self):
        # start screen
        start_screen = pg.display.set_mode(self.size)
        start_screen.fill(settings.BOARD)
        start_screen.blit(START, (5, self.HEIGHT / 6))
        start_screen.blit(BUTTON, (self.WIDTH / 4.4, self.HEIGHT / 1.7))
        pg.display.flip()

        boolean = True
        while boolean:
            pg.event.pump()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == 13:  # press ENTER to start the game
                        self.start_time = pg.time.get_ticks() / 1000
                        boolean = False
                    elif event.key == 27:  # press ESCAPE to quit
                        self.playing = False
                        self.quit()

    def show_summary(self):
        # TODO show summary
        # console summary
        print("\n ### SUMMARY ###")
        game_time = "Game lasted: " + str(self.end_time)
        print(game_time)
        AI_moves = "AI moves: " + str(self.AI.turns)
        print(AI_moves)
        human_moves = "Human moves: " + str(self.human.turns)
        print(human_moves)
        winner = "WINNER: " + self.winner
        print(winner)

        info = [game_time, AI_moves, human_moves, winner]

        i = 0
        for piece in info:
            summary = self.font.render(piece, False, settings.FONT_COLOR)
            self.screen.blit(summary, (self.WIDTH / 5, self.HEIGHT / 2.3 + i))
            i += 60

    @staticmethod
    def convert(fl):
        diff = fl - int(fl)
        milisec = diff * 60

        time = str(int(fl)) + ":" + str(int(milisec))

        return time

    def show_go_screen(self):
        # show end screen and summary
        self.end_time = (pg.time.get_ticks() / 1000) - self.start_time
        self.end_time = self.convert(self.end_time)

        pg.time.wait(1000)  # wait a second...

        go_screen = pg.display.set_mode(self.size)
        go_screen.fill(settings.BOARD)
        go_screen.blit(END, (0, 0))  # SUMMARY sign
        self.show_summary()  # display visual summary

        pg.display.flip()  # refresh the display

        pg.time.wait(5000)  # wait 5 seconds

        self.quit()
