import pygame
from settings import color, FPS
from game import *
from widgets import Button, MessageBox, Notification
import pickle
import threading
from language import lang
from .exit import exit

from .main_screen import MainScreen
from .replay_screen import Replay


pygame.init()
clock = pygame.time.Clock()
pygame.mixer.init()


class OnlineGame(MainScreen):

    def __init__(self, display, size_of_board, side, client):
        MainScreen.__init__(self, display)
        self.side = side
        self.client = client
        self.go_board = Board(size_of_board)
        self.btn_pass = Button(lang.data["pass"], [150, 70], [700, 300])
        self.btn_resign = Button(lang.data["resign"], [150, 70], [700, 425])
        self.show_err_msg = False
        self.request_for_pass = False

    def update_screen(self):
        if self.show_err_msg:
            message_box = MessageBox(
                self.display, lang.data["lost connection"])
            message_box.run()
            del message_box
            self.show = False
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
            elif event.type == pygame.MOUSEBUTTONUP and self.side == self.go_board.turn:
                temp = len(self.go_board.list_of_turns)
                self.go_board.make_step()
                if temp != len(self.go_board.list_of_turns):
                    self.client.client_socket.send(
                        pickle.dumps(self.go_board.list_of_turns[-1]))
        self.display.fill(color['white'])
        self.go_board.draw(self.display)
        self.btn_pass.draw(self.display)
        self.btn_resign.draw(self.display)
        if self.btn_pass.active or self.request_for_pass:
            self.play = self.make_pass(self.display)
            self.btn_pass.active = False
            self.request_for_pass = False
        if self.btn_resign.active:
            self.go_board.list_of_turns.append(None)
            self.client.client_socket.send(pickle.dumps(-1))
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
        if self.go_board.turn ^ self.side:
            text = font.render(lang.data["their turn"], 1, color['green'])
        else:
            text = font.render(lang.data["your turn"], 1, color['green'])
        lbturn = text.get_rect(center=(400, 50))
        self.display.blit(text, lbturn)

    def run_screen(self):
        while self.show:
            self.update_screen()
            pygame.display.update()
            clock.tick(FPS)

    def run_client(self):
        try:
            while True:
                data = self.client.client_socket.recv(1024)
                if data == b'exit':
                    raise EOFError
                if data == b"Get turns":
                    self.client.client_socket.send(pickle.dumps(
                        (self.go_board.size, self.go_board.list_of_turns)))
                else:
                    if self.side != self.go_board.turn:
                        data = pickle.loads(data)
                        if not data:
                            self.request_for_pass = True
                        elif data == -1:
                            self.btn_resign.active = True
                        else:
                            self.go_board.make_step(data)
        except EOFError:
            self.show_err_msg = True

    def run(self):
        thr_screen = threading.Thread(target=self.run_screen)
        thr_client = threading.Thread(target=self.run_client, daemon=True)
        thr_screen.start()
        thr_client.start()
        thr_screen.join()

    def make_pass(self, surface):
        if self.side == self.go_board.turn or self.request_for_pass:
            self.go_board.turn = not self.go_board.turn
            try:
                if not self.go_board.list_of_turns[-1]:
                    self.client.client_socket.send(pickle.dumps(None))
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
                    if not self.request_for_pass:
                        self.client.client_socket.send(pickle.dumps(None))
            except IndexError:
                self.go_board.list_of_turns.append(None)
                if not self.request_for_pass:
                    self.client.client_socket.send(pickle.dumps(None))
            return True
