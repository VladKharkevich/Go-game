import pygame
from settings import display_size
from screens.main_menu_screen import MainMenu


pygame.init()
display = pygame.display.set_mode(display_size)
pygame.display.set_caption('GO')


def rungame():
    screen = MainMenu(display)
    screen.run()


rungame()
