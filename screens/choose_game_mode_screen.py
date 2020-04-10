import pygame
from settings import color
from widgets import Button
from language import lang

from .main_screen import MainScreen
from .choose_size_of_board_screen import ChooseSizeOfBoard
from .watch_go_TV_screen import WatchGoTV


pygame.init()


class ChooseGameMode(MainScreen):

    def __init__(self, display):
        MainScreen.__init__(self, display)
        self.btn_sizes = []
        self.btn_play_with_friend = Button(
            lang.data['play with friend'], [400, 100], [250, 160])
        self.btn_play_online = Button(
            lang.data['play online'], [400, 100], [250, 290])
        self.btn_watch_gotv = Button(
            lang.data['Go TV'], [400, 100], [250, 420])

    def update_screen(self):
        font = pygame.font.Font(None, 72)
        text = font.render(lang.data["choose game mode"], 1, color['green'])
        lb = text.get_rect(center=(450, 50))
        self.display.blit(text, lb)
        self.btn_play_with_friend.draw(self.display)
        self.btn_play_online.draw(self.display)
        self.btn_watch_gotv.draw(self.display)
        if self.btn_play_with_friend.active:
            self.btn_play_with_friend.active = False
            choose_size_of_board = ChooseSizeOfBoard(self.display, 'friend')
            choose_size_of_board.run()
            self.show = False
            del choose_size_of_board
        elif self.btn_play_online.active:
            self.btn_play_online.active = False
            choose_size_of_board = ChooseSizeOfBoard(self.display, 'online')
            choose_size_of_board.run()
            self.show = False
            del choose_size_of_board
        elif self.btn_watch_gotv.active:
            watch_gotv = WatchGoTV(self.display)
            watch_gotv.run()
            self.show = False
            del watch_gotv
