import pygame
from settings import color, FPS
from math import sin, cos, pi
from client import Client
import threading
from language import lang

from .main_screen import MainScreen
from .online_game_screen import OnlineGame


pygame.init()
clock = pygame.time.Clock()


class Waiting(MainScreen):

    def __init__(self, display, size):
        MainScreen.__init__(self, display)
        self.head = 0
        self.temp = 0
        self.size = size
        self.result = None
        self.side = None

    def update_screen(self):
        font = pygame.font.Font(None, 72)
        text = font.render(lang.data["waiting"], 1, color['green'])
        lb = text.get_rect(center=(450, 50))
        self.display.blit(text, lb)
        for angle in range(12):
            if angle == self.head:
                now_color = color['black']
            elif angle == (self.head + 1) % 12:
                now_color = color['dark-gray']
            elif angle == (self.head + 2) % 12:
                now_color = color['gray']
            else:
                now_color = color['light-gray']
            pygame.draw.line(self.display, now_color, (450 + 15 * sin(angle * pi / 6), 300 + 15 * cos(
                angle * pi / 6)), (450 + 30 * sin(angle * pi / 6), 300 + 30 * cos(angle * pi / 6)), 2)
        self.temp += 1
        if self.temp == 5:
            self.temp = 0
            self.head = (self.head - 1) % 12
        if self.result:
            game = OnlineGame(self.display, self.size,
                              int(self.side), self.client)
            game.run()
            del game
            self.show = False

    def run_screen(self):
        while self.show:
            self.update_main_screen()
            pygame.display.update()
            clock.tick(FPS)
        try:
            self.client.client_socket.close()
        except AttributeError:
            pass

    def run_client(self):
        self.client = Client()
        while not self.result:
            self.result, self.side = self.client.start_client(self.size)

    def run(self):
        thr_screen = threading.Thread(target=self.run_screen)
        thr_client = threading.Thread(target=self.run_client, daemon=True)
        thr_client.start()
        thr_screen.start()
        thr_screen.join()
