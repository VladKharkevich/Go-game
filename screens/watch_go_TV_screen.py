import pygame
from settings import color, FPS
from game import *
from widgets import MessageBox, Notification
from client import Client
import pickle
import threading
from language import lang

from .main_screen import MainScreen


pygame.init()
clock = pygame.time.Clock()


class WatchGoTV(MainScreen):
    def __init__(self, display):
        MainScreen.__init__(self, display)
        self.is_traslation_found = True
        self.server_found = True
        self.side = True
        self.start_translation = False
        self.end_of_translation = False

    def update_screen(self):
        self.display.fill(color['white'])
        while self.server_found and self.is_traslation_found and not self.start_translation:
            pass
        if not self.is_traslation_found:
            message_box = MessageBox(
                self.display, lang.data["translation not found"])
            message_box.run()
            del message_box
            self.show = False
        elif not self.server_found:
            message_box = MessageBox(
                self.display, lang.data["server not found"])
            message_box.run()
            del message_box
            self.show = False
        else:
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
            self.go_board.draw(self.display)
            font = pygame.font.Font(None, 72)
            if self.side:
                text = font.render(
                    lang.data["black's turn"], 1, color['green'])
            else:
                text = font.render(
                    lang.data["white's turn"], 1, color['green'])
            lbturn = text.get_rect(center=(400, 50))
            self.display.blit(text, lbturn)
            font = pygame.font.Font(None, 45)
            text = font.render(
                lang.data["Go TV"], 1, color['black'])
            lbturn = text.get_rect(center=(800, 50))
            self.display.blit(text, lbturn)
            if self.end_of_translation:
                if event.key == pygame.K_ESCAPE:
                    notification = Notification(
                        self.display, lang.data["end of translation"])
                    notification.run()
                    if notification.action:
                        self.show = False
                    del notification

    def run_screen(self):
        while self.show:
            self.update_main_screen()
            pygame.display.update()
            clock.tick(FPS)
        self.client.client_socket.close()

    def run_client(self):
        self.client = Client("gotv")
        if self.client.access:
            data = self.client.connect_to_go_TV()
            print(data)
            if data == "Translation not found":
                self.is_traslation_found = False
            else:
                self.go_board = Board(data[0])
                self.list_of_turns = data[1]
                self.side = (len(self.list_of_turns) + 1) % 2
                for turn in self.list_of_turns:
                    self.go_board.make_step(turn)
                self.start_translation = True
                while True:
                    data = self.client.client_socket.recv(1024)
                    if data == b'exit' or not data:
                        self.show = False
                    elif data == b"end_of_translation":
                        self.end_of_translation = True
                    else:
                        self.side ^= 1
                        data = pickle.loads(data)
                        self.go_board.make_step(data)
        else:
            self.server_found = False

    def run(self):
        thr_screen = threading.Thread(target=self.run_screen)
        thr_client = threading.Thread(target=self.run_client, daemon=True)
        thr_client.start()
        thr_screen.start()
        thr_screen.join()
