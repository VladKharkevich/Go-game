import os
import pygame
from settings import color, sound
from game import *
from widgets import Button, Notification
from language import lang
from .exit import exit

from .main_screen import MainScreen
from .replay_screen import Replay


pygame.init()
pygame.mixer.init()


class Game(MainScreen):

    def __init__(self, display, size_of_board):
        MainScreen.__init__(self, display)
        self.go_board = Board(size_of_board)
        self.btn_pass = Button(lang.data["pass"], [170, 70], [690, 300])
        self.btn_resign = Button(lang.data["resign"], [170, 70], [690, 425])
        self.sound = pygame.mixer.Sound(os.path.join('sounds/gong.wav'))
        if sound:
            self.sound.play()

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(self.display)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    notification = Notification(
                        self.display, lang.data["exit to menu"])
                    notification.run()
                    if notification.action:
                        self.show = False
                    del notification
            elif event.type == pygame.MOUSEBUTTONUP:
                self.go_board.make_step()
        self.display.fill(color['white'])
        self.go_board.draw(self.display)
        self.btn_pass.draw(self.display)
        self.btn_resign.draw(self.display)
        if self.btn_pass.active:
            self.play = self.make_pass(self.display)
            self.btn_pass.active = False
        if self.btn_resign.active:
            self.go_board.list_of_turns.append(None)
            notification = Notification(
                self.display, lang.data["game over"])
            notification.run()
            if notification.action:
                replay = Replay(
                    self.display, self.go_board.list_of_turns, self.go_board.size)
                replay.run()
                del replay
                self.show = False
            del notification
        font = pygame.font.Font(None, 72)
        if self.go_board.turn:
            text = font.render(lang.data["black's turn"], 1, color['green'])
        else:
            text = font.render(lang.data["white's turn"], 1, color['green'])
        lbturn = text.get_rect(center=(400, 50))
        self.display.blit(text, lbturn)

    def update_main_screen(self):
        self.update_screen()

    def make_pass(self, surface):
        self.go_board.turn = not self.go_board.turn
        try:
            if not self.go_board.list_of_turns[-1]:
                notification = Notification(
                    surface, lang.data["game over"])
                notification.run()
                if notification.action:
                    replay = Replay(
                        surface, self.go_board.list_of_turns, self.go_board.size)
                    replay.run()
                    del replay
                    self.show = False
                del notification
                return False
            else:
                self.go_board.list_of_turns.append(None)
        except IndexError:
            self.go_board.list_of_turns.append(None)
        return True
