import pygame
from settings import color, FPS
from widgets import Notification
from language import lang
from .exit import exit


pygame.init()
clock = pygame.time.Clock()


class MainScreen:

    def __init__(self, display):
        self.display = display
        self.show = True

    def update_main_screen(self):
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
        self.display.fill(color['white'])
        self.update_screen()

    def update_screen(self):
        pass

    def run(self):
        while self.show:
            self.update_main_screen()
            pygame.display.update()
            clock.tick(FPS)
