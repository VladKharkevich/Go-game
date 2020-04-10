import pygame
from settings import color, FPS
from widgets import Button
from language import lang
from .exit import exit

from .choose_game_mode_screen import ChooseGameMode
from .settings_screen import Settings


pygame.init()
clock = pygame.time.Clock()


class MainMenu:

    def __init__(self, display):
        self.display = display
        self.btn_start = Button(lang.data["start"], [220, 70], [340, 150])
        self.btn_settings = Button(
            lang.data["settings"], [220, 70], [340, 250])
        self.btn_exit = Button(lang.data["exit"], [220, 70], [340, 350])

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(self.display)
        self.display.fill(color['white'])
        self.btn_start.draw(self.display)
        self.btn_settings.draw(self.display)
        self.btn_exit.draw(self.display)
        if self.btn_start.active:
            choose_size_of_board = ChooseGameMode(self.display)
            choose_size_of_board.run()
            del choose_size_of_board
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
