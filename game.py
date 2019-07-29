import pygame
from settings import color, FPS
import os, sys
from widgets import Button, Notification, Toggle


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

    def make_pass(self, surface):
        self.turn = not self.turn
        try:
            if not self.list_of_turns[-1]:
                notification = Notification(surface, 'Game over. Do you want back to see replay?')
                notification.run()
                if notification.action:
                    replay = Replay(surface, self.list_of_turns)
                    replay.run()
                    del replay
                else:
                    return False
                del notification
            else: 
                self.list_of_turns.append(None)
        except IndexError:
            self.list_of_turns.append(None)
        return True


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
                    notification = Notification(self.display, 'Do you really want back to main menu?')
                    notification.run()
                    if notification.action:
                        self.play = False
                    del notification
        self.display.fill(color['white'])
        self.go_board.draw(self.display)
        self.btn_pass.draw(self.display)
        if self.btn_pass.active:
            self.play = self.go_board.make_pass(self.display)
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
        self.btn_about_program = Button('program', [170, 50], [375, 250], 40)
        self.btn_rools = Button('rools', [170, 50], [375, 320], 40)
        self.btn_main_menu = Button('main menu', [170, 50], [375, 390], 40)
        self.tgl_music = Toggle([250, 130])
        self.tgl_sound = Toggle([650, 130])
        self.show = True

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(self.display)
        font = pygame.font.Font(None, 44)
        self.display.fill(color['white'])
        self.btn_about_program.draw(self.display)
        self.btn_rools.draw(self.display)
        self.btn_main_menu.draw(self.display)
        self.tgl_music.draw(self.display)
        self.tgl_sound.draw(self.display)
        text_music = font.render("Music", 1, color['black'])
        text_sound = font.render("Sound", 1, color['black'])
        lbmusic = text_music.get_rect(center=(280, 100))
        lbsound = text_sound.get_rect(center=(680, 100))
        self.display.blit(text_music, lbmusic)
        self.display.blit(text_sound, lbsound)
        if self.btn_main_menu.active:
            self.show = False

    def run(self):
        while self.show:
            self.update_screen()
            pygame.display.update()
            clock.tick(FPS)


class Replay:

    def __init__(self, display, list_of_turns):
        self.list_of_turns = list_of_turns
        self.current_step = 0
        self.display = display
        self.show = True
        self.go_board = Board(19)
        self.btn_prev = Button('prev', [150, 70], [700, 300])
        self.btn_next = Button('next', [150, 70], [700, 400])

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(self.display)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    notification = Notification(self.display, 'Do you really want back to main menu?')
                    notification.run()
                    if notification.action:
                        self.show = False
                    del notification
        self.display.fill(color['white'])
        self.go_board.draw(self.display)
        self.btn_prev.draw(self.display)
        self.btn_next.draw(self.display)
        if self.btn_next.active:
            if self.current_step < len(self.list_of_turns) - 1:
                self.make_step_forward()
            self.btn_next.active = False
        if self.btn_prev.active:
            if self.current_step > 0:
                self.make_step_back()
            self.btn_prev.active = False

    def make_step_forward(self):
        coord = self.list_of_turns[self.current_step]
        if coord:
            if self.current_step % 2 == 0:
                self.go_board.board[coord[0]][coord[1]] = 'black'
            else:
                self.go_board.board[coord[0]][coord[1]] = 'white'
        self.current_step += 1

    def make_step_back(self):
        self.current_step -= 1
        coord = self.list_of_turns[self.current_step]
        if coord:
            self.go_board.board[coord[0]][coord[1]] = None

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
