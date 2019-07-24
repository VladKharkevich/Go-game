import pygame
from settings import color
import os


pygame.init()


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


class Button:

    def __init__(self, name, size, pos):
        self.name = name
        self.size = size
        self.pos = pos
        self.is_pressed = False
        self.is_click = False
        self.action = False

    def draw_button(self, surface):
        if (not pygame.mouse.get_pressed()[0] and self.is_pressed and 
             self.mouse_on_button()):
            self.action = True
        self.click_button()
        if self.mouse_on_button() and self.is_pressed:
            pygame.draw.rect(surface, color['green'], (self.pos[0],
                 self.pos[1], self.size[0], self.size[1]))
        else:
            pygame.draw.rect(surface, color['brown'], (self.pos[0],
                 self.pos[1], self.size[0], self.size[1]))
        font = pygame.font.Font(None, 60)
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

    def btn_function(self):
        self.action = False


class ButtonPass(Button):
    def btn_function(self, board):
        board.turn = not board.turn
        board.list_of_turns.append(None)
        self.action = False
