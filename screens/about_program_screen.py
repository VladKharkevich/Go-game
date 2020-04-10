import pygame
from settings import color
from widgets import Button
from language import lang

from .main_screen import MainScreen


pygame.init()


class AboutProgram(MainScreen):

    def __init__(self, display):
        MainScreen.__init__(self, display)
        self.btn_main_menu = Button(lang.data["main menu"], [
                                    240, 50], [340, 480], 38)

    def update_screen(self):
        font = pygame.font.Font(None, 52)
        mdl_font = pygame.font.Font(None, 40)
        sm_font = pygame.font.SysFont('arial', 25)
        text = font.render(lang.data["about program"], 1, color['green'])
        lb = text.get_rect(center=(450, 50))
        self.display.blit(text, lb)
        text = mdl_font.render(lang.data["go"], 1, color['black'])
        lb = text.get_rect(center=(450, 150))
        self.display.blit(text, lb)
        text = sm_font.render("0.1.0", 1, color['black'])
        lb = text.get_rect(center=(450, 200))
        self.display.blit(text, lb)
        text = sm_font.render(
            lang.data["popular Japanese game"], 1, color['black'])
        lb = text.get_rect(center=(450, 250))
        self.display.blit(text, lb)
        text = sm_font.render(lang.data["developer"], 1, color['black'])
        lb = text.get_rect(center=(450, 320))
        self.display.blit(text, lb)
        text = sm_font.render(lang.data["copyright"], 1, color['black'])
        lb = text.get_rect(center=(450, 370))
        self.display.blit(text, lb)
        self.btn_main_menu.draw(self.display)
        if self.btn_main_menu.active:
            self.show = False
