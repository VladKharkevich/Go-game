import pygame
from settings import color
from widgets import Button
from language import lang

from .main_screen import MainScreen
from .game_screen import Game
from .waiting_screen import Waiting


pygame.init()


class ChooseSizeOfBoard(MainScreen):

    def __init__(self, display, mode):
        MainScreen.__init__(self, display)
        sizes = [5, 6, 7, 8, 9, 11, 13, 15, 19]
        self.btn_sizes = []
        for i in range(len(sizes)):
            self.btn_sizes.append(Button('%dx%d' % (sizes[i], sizes[i]), [120, 120], [
                                  150 * (i % 3) + 200, 150 * (i // 3) + 100]))
        self.show = True
        self.mode = mode

    def update_screen(self):
        font = pygame.font.Font(None, 72)
        text = font.render(lang.data["size of board"], 1, color['green'])
        lb = text.get_rect(center=(450, 50))
        self.display.blit(text, lb)
        for btn_size in self.btn_sizes:
            btn_size.draw(self.display)
            if btn_size.active:
                btn_size.active = False
                if self.mode == 'friend':
                    game = Game(self.display, int(
                        btn_size.name.split('x')[0]))
                    game.run()
                    del game
                elif self.mode == 'online':
                    waiting = Waiting(self.display, int(
                        btn_size.name.split('x')[0]))
                    waiting.run()
                    del waiting
                self.show = False
