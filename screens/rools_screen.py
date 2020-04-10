import pygame
import os
from widgets import Button, Slider
from language import lang

from .main_screen import MainScreen


pygame.init()


class Rools(MainScreen):

    def __init__(self, display):
        MainScreen.__init__(self, display)
        self.btn_main_menu = Button(lang.data["main menu"], [
                                    240, 50], [340, 530], 38)
        self.slider = Slider()
        image_rool = pygame.image.load(os.path.join('images/rools.png'))
        self.image_rool = pygame.transform.scale(
            image_rool, (800, image_rool.get_height() * 800 // image_rool.get_width()))

    def update_screen(self):
        image = pygame.transform.chop(
            self.image_rool, (0, 0, 0, (self.slider.value / 100) * (self.image_rool.get_height() - 500)))
        image = pygame.transform.chop(
            image, (0, 500, 0, image.get_height() - 500))
        self.display.blit(image, (20, 20))
        self.btn_main_menu.draw(self.display)
        self.slider.draw(self.display)
        if self.btn_main_menu.active:
            self.show = False
