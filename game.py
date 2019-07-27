import pygame
from settings import color, FPS
import os, sys
from widgets import Button, Notification


pygame.init()
clock = pygame.time.Clock()


class Board:

    def __init__(self, size):
        self.size = size
        self.board = [[None for i in range(size)] for j in range(size)]
        self.list_of_turns = []
        black_stone = pygame.image.load(os.path.join('images/black.png'))
        white_stone = pygame.image.load(os.path.join('images/white.png'))
        self.black_stone = pygame.transform.scale(black_stone,
                                                  (black_stone.get_width() // 4,
                                                   black_stone.get_height() // 4))
        self.white_stone = pygame.transform.scale(white_stone,
                                                  (white_stone.get_width() // 4,
                                                   white_stone.get_height() // 4))
        self.turn = True

    def draw(self, surface):
        pygame.draw.rect(surface, color['brown'],
                         (150, 80, 30 + 18 * 25, 30 + 18 * 25))
        for i in range(self.size):
            pygame.draw.line(surface, color['black'],
                             (165 + 25 * i, 95), (165 + 25 * i, 545), 3)
            pygame.draw.line(surface, color['black'],
                             (165, 95 + 25 * i), (615, 95 + 25 * i), 3)
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 'black':
                    surface.blit(self.black_stone, (152 + 25 * i, 82 + 25 * j))
                elif self.board[i][j] == 'white':
                    surface.blit(self.white_stone, (152 + 25 * i, 82 + 25 * j))

    def make_step(self):
        pos = pygame.mouse.get_pos()
        coord = self.find_coordinates(pos)
        if coord:
            if self.turn:
                self.board[coord[0]][coord[1]] = 'black'
            else:
                self.board[coord[0]][coord[1]] = 'white'
            self.list_of_turns.append(coord)
            self.turn = not self.turn

    def find_coordinates(self, pos):
        if (pos[0] in range(160, 621)) and (pos[1] in range(90, 551)) and (
                pos[0] % 25 > 10 or pos[0] % 25 < 20) and (pos[1] % 25 > 15):
            coord = [(pos[0] - 160) // 25, (pos[1] - 90) // 25]
            if not self.board[coord[0]][coord[1]]:
                return coord
        return None

    def make_pass(self):
        self.turn = not self.turn
        self.list_of_turns.append(None)


class Game:

    def __init__(self, display):
        self.display = display
        self.go_board = Board(19)
        self.btn_pass = Button('pass', [150, 70], [700, 300])
        self.play = True

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(self.display)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.go_board.make_step()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    notification = Notification(self.display, 'Are you really want back to main menu?')
                    notification.run()
                    if notification.action:
                        self.play = False
                    del notification
                    # self.play = False
        self.display.fill(color['white'])
        self.go_board.draw(self.display)
        self.btn_pass.draw(self.display)
        if self.btn_pass.active:
            self.go_board.make_pass()
            self.btn_pass.active = False
        font = pygame.font.Font(None, 72)
        if self.go_board.turn:
            text = font.render("Black's turn", 1, color['green'])
        else:
            text = font.render("White's turn", 1, color['green'])
        lbturn = text.get_rect(center=(400, 50))
        self.display.blit(text, lbturn)

    def run(self):
        while self.play:
            self.update_screen()
            pygame.display.update()
            clock.tick(FPS)


class MainMenu():

    def __init__(self, display):
        self.display = display
        self.btn_start = Button('start', [220, 70], [340, 150])
        self.btn_settings = Button('settings', [220, 70], [340, 250])
        self.btn_exit = Button('exit', [220, 70], [340, 350])

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(self.display)
        self.display.fill(color['white'])
        self.btn_start.draw(self.display)
        self.btn_settings.draw(self.display)
        self.btn_exit.draw(self.display)
        if self.btn_start.active:
            game = Game(self.display)
            game.run()
            del game
            self.btn_start.active = False
        elif self.btn_settings.active:
            settings = Settings(self.display)
            settings.run()
            del settings
            self.btn_settings.active = False
        elif self.btn_exit.active:
            exit(self.display)
            self.btn_exit.active = False

    def run(self):
        while True:
            self.update_screen()
            pygame.display.update()
            clock.tick(FPS)


class Settings:

    def __init__(self, display):
        self.display = display
        self.btn_about_program = Button('program', [220, 70], [340, 200])
        self.btn_rools = Button('rools', [220, 70], [340, 300])
        self.btn_main_menu = Button('main menu', [220, 70], [340, 400])
        self.show = True

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(self.display)
        self.display.fill(color['white'])
        self.btn_about_program.draw(self.display)
        self.btn_rools.draw(self.display)
        self.btn_main_menu.draw(self.display)
        if self.btn_main_menu.active:
            self.show = False


    def run(self):
        while self.show:
            self.update_screen()
            pygame.display.update()
            clock.tick(FPS)


def exit(display):
    notification = Notification(display, 'Are you really want to exit?')
    notification.run()
    if notification.action:
        pygame.quit()
        quit()
    del notification