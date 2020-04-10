import pygame
from game import *
from widgets import Button
from language import lang

from .main_screen import MainScreen


pygame.init()
clock = pygame.time.Clock()


class Replay(MainScreen):

    def __init__(self, display, list_of_turns, size):
        MainScreen.__init__(self, display)
        self.list_of_turns = list_of_turns
        self.current_step = 0
        self.go_board = Board(size)
        self.size = size
        self.btn_prev = Button(lang.data["prev"], [150, 70], [700, 300])
        self.btn_next = Button(lang.data["next"], [150, 70], [700, 400])

    def update_screen(self):
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
        self.go_board.make_step(coord)
        self.current_step += 1

    def make_step_back(self):
        self.current_step -= 1
        self.go_board.__init__(self.size)
        for step in range(self.current_step):
            coord = self.list_of_turns[step]
            self.go_board.make_step(coord)
