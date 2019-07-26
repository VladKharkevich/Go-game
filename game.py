import pygame
from settings import color, FPS
import os, sys


pygame.init()
clock = pygame.time.Clock()

class Board:

    def __init__(self, size):
        self.size = size
        self.board = [[None for i in range(size)] for j in range(size)]
        self.list_of_turns = []
        black_stone = pygame.image.load(os.path.join('images/black.png'))
        white_stone = pygame.image.load(os.path.join('images/white.png'))
        self.black_stone = pygame.transform.scale(black_stone,
                                                  (black_stone.get_width() // 4,
                                                   black_stone.get_height() // 4))
        self.white_stone = pygame.transform.scale(white_stone,
                                                  (white_stone.get_width() // 4,
                                                   white_stone.get_height() // 4))
        self.turn = True

    def draw_board(self, surface):
        pygame.draw.rect(surface, color['brown'],
                         (150, 80, 30 + 18 * 25, 30 + 18 * 25))
        for i in range(self.size):
            pygame.draw.line(surface, color['black'],
                             (165 + 25 * i, 95), (165 + 25 * i, 545), 3)
            pygame.draw.line(surface, color['black'],
                             (165, 95 + 25 * i), (615, 95 + 25 * i), 3)
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 'black':
                    surface.blit(self.black_stone, (152 + 25 * i, 82 + 25 * j))
                elif self.board[i][j] == 'white':
                    surface.blit(self.white_stone, (152 + 25 * i, 82 + 25 * j))

    def make_step(self):
        pos = pygame.mouse.get_pos()
        coord = self.find_coordinates(pos)
        if coord:
            if self.turn:
                self.board[coord[0]][coord[1]] = 'black'
            else:
                self.board[coord[0]][coord[1]] = 'white'
            self.list_of_turns.append(coord)
            self.turn = not self.turn

    def find_coordinates(self, pos):
        if (pos[0] in range(160, 621)) and (pos[1] in range(90, 551)) and (
                pos[0] % 25 > 10 or pos[0] % 25 < 20) and (pos[1] % 25 > 15):
            coord = [(pos[0] - 160) // 25, (pos[1] - 90) // 25]
            if not self.board[coord[0]][coord[1]]:
                return coord
        return None

    def make_pass(self):
        self.turn = not self.turn
        self.list_of_turns.append(None)


class Button:

    def __init__(self, name, size, pos):
        self.name = name
        self.size = size
        self.pos = pos
        self.is_pressed = False
        self.is_click = False
        self.active = False

    def draw_button(self, surface):
        if (not pygame.mouse.get_pressed()[0] and self.is_pressed and 
             self.mouse_on_button()):
            self.active = True
        self.click_button()
        if self.mouse_on_button() and self.is_pressed:
            pygame.draw.rect(surface, color['green'], (self.pos[0],
                 self.pos[1], self.size[0], self.size[1]))
        else:
            pygame.draw.rect(surface, color['brown'], (self.pos[0],
                 self.pos[1], self.size[0], self.size[1]))
        font = pygame.font.Font(None, 54)
        text_pass = font.render(self.name.upper(), 1, color['white'])
        lb_pass = text_pass.get_rect(center=[self.pos[i] + self.size[i] / 2
                                             for i in range(2)])
        surface.blit(text_pass, lb_pass)

    def click_button(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.is_click:
                self.is_click = True
                if self.mouse_on_button():
                    self.is_pressed = True
        else:
            self.is_click = False
            self.is_pressed = False

    def mouse_on_button(self):
        if (pygame.mouse.get_pos()[0] in range(self.pos[0],
             self.pos[0] + self.size[0])) and (pygame.mouse.get_pos()[1]
             in range(self.pos[1], self.pos[1] + self.size[1])):
            return True
        return False


class Game:

    def __init__(self, display):
        self.display = display
        self.go_board = Board(19)
        self.btn_pass = Button('pass', [150, 70], [700, 300])
        self.play = True

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.go_board.make_step()
            elif event.type== pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.play = False
        self.display.fill(color['white'])
        self.go_board.draw_board(self.display)
        self.btn_pass.draw_button(self.display)
        if self.btn_pass.active:
            self.go_board.make_pass()
            self.btn_pass.active = False
        font = pygame.font.Font(None, 72)
        if self.go_board.turn:
            text = font.render("Black's turn", 1, color['green'])
        else:
            text = font.render("White's turn", 1, color['green'])
        lbturn = text.get_rect(center=(400, 50))
        self.display.blit(text, lbturn)

    def run(self):
        while self.play:
            self.update_screen()
            pygame.display.update()
            clock.tick(FPS)


class MainMenu():

    def __init__(self, display):
        self.display = display
        self.btn_start = Button('start', [200, 70], [350, 150])
        self.btn_settings = Button('settings', [200, 70], [350, 250])
        self.btn_exit = Button('exit', [200, 70], [350, 350])

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 
        self.display.fill(color['white'])
        self.btn_start.draw_button(self.display)
        self.btn_settings.draw_button(self.display)
        self.btn_exit.draw_button(self.display)
        if self.btn_start.active:
            game = Game(self.display)
            game.run()
            del game
            self.btn_start.active = False
        elif self.btn_exit.active:
            sys.exit()


    def run(self):
        while True:
            self.update_screen()
            pygame.display.update()
            clock.tick(FPS)
