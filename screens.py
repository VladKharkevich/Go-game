import pygame
from settings import color, FPS, sound
from game import *
from widgets import *
from math import sin, cos, pi
from client import Client
import pickle
import threading
from language import lang


pygame.init()
clock = pygame.time.Clock()
pygame.mixer.init()


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


class Game(MainScreen):

    def __init__(self, display, size_of_board):
        MainScreen.__init__(self, display)
        self.go_board = Board(size_of_board)
        self.btn_pass = Button(lang.data["pass"], [170, 70], [690, 300])
        self.btn_resign = Button(lang.data["resign"], [170, 70], [690, 425])
        self.sound = pygame.mixer.Sound(os.path.join('sounds/gong.wav'))
        if sound:
            self.sound.play()

    def update_screen(self):
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
            elif event.type == pygame.MOUSEBUTTONUP:
                self.go_board.make_step()
        self.display.fill(color['white'])
        self.go_board.draw(self.display)
        self.btn_pass.draw(self.display)
        self.btn_resign.draw(self.display)
        if self.btn_pass.active:
            self.play = self.make_pass(self.display)
            self.btn_pass.active = False
        if self.btn_resign.active:
            self.go_board.list_of_turns.append(None)
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
        if self.go_board.turn:
            text = font.render(lang.data["black's turn"], 1, color['green'])
        else:
            text = font.render(lang.data["white's turn"], 1, color['green'])
        lbturn = text.get_rect(center=(400, 50))
        self.display.blit(text, lbturn)

    def update_main_screen(self):
        self.update_screen()

    def make_pass(self, surface):
        self.go_board.turn = not self.go_board.turn
        try:
            if not self.go_board.list_of_turns[-1]:
                winner = self.go_board.find_winner()
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
        except IndexError:
            self.go_board.list_of_turns.append(None)
        return True


class MainMenu:

    def __init__(self, display):
        self.display = display
        self.btn_start = Button(lang.data["start"], [220, 70], [340, 150])
        self.btn_settings = Button(lang.data["settings"], [220, 70], [340, 250])
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


class Settings(MainScreen):

    def __init__(self, display):
        MainScreen.__init__(self, display)
        self.btn_about_program = Button(lang.data["program"], [240, 50], [340, 270], 38)
        self.btn_rools = Button(lang.data["rools"], [240, 50], [340, 340], 38)
        self.btn_main_menu = Button(lang.data["main menu"], [240, 50], [340, 410], 38)
        self.tgl_music = Toggle([250, 130])
        self.tgl_sound = Toggle([650, 130])
        self.tgl_language = Toggle([420, 200])
        if lang.current_language == 'russian':
            self.tgl_language.active = True
        if sound:
            self.tgl_sound.active = True

    def update_screen(self):
        font = pygame.font.Font(None, 44)
        self.btn_about_program.draw(self.display)
        self.btn_rools.draw(self.display)
        self.btn_main_menu.draw(self.display)
        self.tgl_music.draw(self.display)
        self.tgl_sound.draw(self.display)
        self.tgl_language.draw(self.display)
        text_music = font.render(lang.data["music"], 1, color['black'])
        text_sound = font.render(lang.data["sound"], 1, color['black'])
        text_russian = font.render("Русский", 1, color['black'])
        text_english = font.render("English", 1, color['black'])
        lbmusic = text_music.get_rect(center=(280, 100))
        lbsound = text_sound.get_rect(center=(680, 100))
        lbrussian = text_russian.get_rect(center=(590, 210))
        lbenglish = text_russian.get_rect(center=(310, 210))
        self.display.blit(text_music, lbmusic)
        self.display.blit(text_sound, lbsound)
        self.display.blit(text_russian, lbrussian)
        self.display.blit(text_english, lbenglish)
        if self.btn_main_menu.active:
            self.show = False
        elif self.btn_rools.active:
            rools = Rools(self.display)
            rools.run()
            del rools
            self.btn_rools.active = False
        elif self.btn_about_program.active:
            about_program = AboutProgram(self.display)
            about_program.run()
            del about_program
            self.btn_about_program.active = False
        if self.tgl_language.active and lang.current_language != 'russian':
            lang.change_language('russian')
        if not self.tgl_language.active and lang.current_language != 'english':
            lang.change_language('english')
        global sound
        if self.tgl_sound.active:
            sound = True
        else:
            sound = False


class Rools(MainScreen):

    def __init__(self, display):
        MainScreen.__init__(self, display)
        self.btn_main_menu = Button(lang.data["main menu"], [240, 50], [340, 530], 38)
        self.slider = Slider()
        image_rool = pygame.image.load(os.path.join('images/rools.png'))
        self.image_rool = pygame.transform.scale(image_rool, (800, image_rool.get_height() * 800 // image_rool.get_width()))

    def update_screen(self):
        image = pygame.transform.chop(self.image_rool, (0, 0, 0, (self.slider.value / 100) * (self.image_rool.get_height() - 500)))
        image = pygame.transform.chop(image, (0, 500, 0, image.get_height() - 500))
        self.display.blit(image, (20, 20))
        self.btn_main_menu.draw(self.display)
        self.slider.draw(self.display)
        if self.btn_main_menu.active:
            self.show = False


class AboutProgram(MainScreen):

    def __init__(self, display):
        MainScreen.__init__(self, display)
        self.btn_main_menu = Button(lang.data["main menu"], [240, 50], [340, 480], 38)

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
        text = sm_font.render(lang.data["popular Japanese game"], 1, color['black'])
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


class Replay(MainScreen):

    def __init__(self, display, list_of_turns, size):
        MainScreen.__init__(self, display)
        self.list_of_turns = list_of_turns
        self.current_step = 0
        self.go_board = Board(size)
        self.size = size
        self.btn_prev = Button(lang.data["prev"], [150, 70], [700, 300])
        self.btn_next = Button(lang.data["next"], [150, 70], [700, 400])

    def update_screen(self):
        self.go_board.draw(self.display)
        self.btn_prev.draw(self.display)
        self.btn_next.draw(self.display)
        if self.btn_next.active:
            if self.current_step < len(self.list_of_turns) - 1:
                self.make_step_forward()
            self.btn_next.active = False
        if self.btn_prev.active:
            if self.current_step > 0:
                self.make_step_back()
            self.btn_prev.active = False

    def make_step_forward(self):
        coord = self.list_of_turns[self.current_step]
        self.go_board.make_step(coord)
        self.current_step += 1

    def make_step_back(self):
        self.current_step -= 1
        self.go_board.__init__(self.size)
        for step in range(self.current_step):
            coord = self.list_of_turns[step]
            self.go_board.make_step(coord)


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


class ChooseGameMode(MainScreen):

    def __init__(self, display):
        MainScreen.__init__(self, display)
        self.btn_sizes = []
        self.btn_play_with_friend = Button(
            lang.data['play with friend'], [400, 100], [250, 220])
        self.btn_play_online = Button(lang.data['play online'], [400, 100], [250, 350])

    def update_screen(self):
        font = pygame.font.Font(None, 72)
        text = font.render(lang.data["choose game mode"], 1, color['green'])
        lb = text.get_rect(center=(450, 50))
        self.display.blit(text, lb)
        self.btn_play_with_friend.draw(self.display)
        self.btn_play_online.draw(self.display)
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
            game = OnlineGame(self.display, self.size, int(self.side), self.client)
            game.run()
            del game
            self.show = False

    def run_screen(self):
        while self.show:
            self.update_main_screen()
            pygame.display.update()
            clock.tick(FPS)
        self.client.client_socket.close()

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
                    self.client.client_socket.send(pickle.dumps(self.go_board.list_of_turns[-1]))
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


def exit(display):
    notification = Notification(display, lang.data["exit game"])
    notification.run()
    if notification.action:
        pygame.quit()
        quit()
    del notification
