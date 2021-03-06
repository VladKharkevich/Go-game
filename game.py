import pygame
import os
from settings import color
import copy


pygame.init()


class Board:

    def __init__(self, size):
        self.size = size
        self.board = [[None for i in range(size)] for j in range(size)]
        self.temp_for_rool_co = [[[None for i in range(size)] for j in range(size)],
                                 [[None for i in range(size)] for j in range(size)]]
        self.turn = True
        self.list_of_turns = []
        self.dist_between_lines = 450 // (self.size - 1)
        image_w = pygame.image.load(os.path.join('images/white.png'))
        self.image_w = pygame.transform.scale(image_w,
                                              ((image_w.get_width() * self.dist_between_lines) // 100,
                                               (image_w.get_height() * self.dist_between_lines) // 100))
        image_b = pygame.image.load(os.path.join('images/black.png'))
        self.image_b = pygame.transform.scale(image_b,
                                              ((image_b.get_width() * self.dist_between_lines) // 100,
                                               (image_b.get_height() * self.dist_between_lines) // 100))

    def draw(self, surface):
        pygame.draw.rect(surface, color['brown'],
                         (150, 80, 480, 480))
        for i in range(self.size):
            pygame.draw.line(surface, color['black'],
                             (165 + self.dist_between_lines * i, 95), (165 + self.dist_between_lines * i, 545), 3)
            pygame.draw.line(surface, color['black'],
                             (165, 95 + self.dist_between_lines * i), (615, 95 + self.dist_between_lines * i), 3)
        for i in range(self.size):
            for j in range(self.size):
                if type(self.board[i][j]) == BlackStone:
                    surface.blit(self.image_b,
                                 (165 - (self.dist_between_lines // 2) + self.dist_between_lines * i, 95 - (self.dist_between_lines // 2) + self.dist_between_lines * j))
                elif type(self.board[i][j]) == WhiteStone:
                    surface.blit(self.image_w,
                                 (165 - (self.dist_between_lines // 2) + self.dist_between_lines * i, 95 - (self.dist_between_lines // 2) + self.dist_between_lines * j))

    def make_step(self, coord=None):
        if not coord:
            pos = pygame.mouse.get_pos()
            coord = self.find_coordinates(pos)
        if coord:
            liberty = self.count_liberty(coord)
            if self.turn:
                self.board[coord[0]][coord[1]] = BlackStone(liberty)
            else:
                self.board[coord[0]][coord[1]] = WhiteStone(liberty)
            self.change_liberty(coord, '-')
            neigh_points = self.find_neigh_points(coord)
            if liberty > 0:
                turn = True
                for point in neigh_points:
                    if type(self.board[point[0]][point[1]]) != type(self.board[coord[0]][coord[1]]) and self.board[point[0]][point[1]]:
                        self.temp = []
                        if not self.stone_is_alive(point):
                            for elem in self.temp:
                                self.board[elem[0]][elem[1]] = None
                                self.change_liberty(elem, '+')
            else:
                turn = False
                for point in neigh_points:
                    if type(self.board[point[0]][point[1]]) == type(self.board[coord[0]][coord[1]]):
                        self.temp = []
                        if self.stone_is_alive(point):
                            turn = True
                    elif type(self.board[point[0]][point[1]]) != type(self.board[coord[0]][coord[1]]) and self.board[point[0]][point[1]]:
                        self.temp = []
                        if not self.stone_is_alive(point):
                            for elem in self.temp:
                                turn = True
                                self.board[elem[0]][elem[1]] = None
                                self.change_liberty(elem, '+')
            if turn:
                if not self.rool_co():
                    self.list_of_turns.append(coord)
                    self.turn = not self.turn
                    self.temp_for_rool_co[0], self.temp_for_rool_co[1] = (
                        self.temp_for_rool_co[1], self.temp_for_rool_co[0])
                    self.temp_for_rool_co[1] = copy.deepcopy(self.board)
                else:
                    self.board = copy.deepcopy(self.temp_for_rool_co[1])
            else:
                self.board[coord[0]][coord[1]] = None
                self.change_liberty(coord, '+')

    def rool_co(self):
        if len(self.temp_for_rool_co) > 1:
            if self.board_are_equil():
                self.board = copy.deepcopy(self.temp_for_rool_co[0])
                return True
        return False

    def board_are_equil(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if type(self.board[i][j]) != type(self.temp_for_rool_co[0][i][j]):
                    return False
        return True

    def stone_is_alive(self, coord):
        if self.count_liberty(coord) == 0:
            self.temp.append(coord)
            neigh_points = self.find_neigh_points(coord)
            for point in neigh_points:
                if (point not in self.temp) and (type(self.board[point[0]][point[1]]) == type(self.board[coord[0]][coord[1]])):
                    if self.stone_is_alive(point):
                        return True
        else:
            return True

    def find_coordinates(self, pos):
        pos = [pos[0] - 165, pos[1] - 95]
        if (pos[0] % self.dist_between_lines < self.dist_between_lines * 0.3 or pos[0] % self.dist_between_lines > self.dist_between_lines * 0.7) and (
                pos[0] % self.dist_between_lines < self.dist_between_lines * 0.3 or pos[0] % self.dist_between_lines > self.dist_between_lines * 0.7):
            coord = [(pos[0] + self.dist_between_lines // 2) // self.dist_between_lines,
                     (pos[1] + self.dist_between_lines // 2) // self.dist_between_lines]
            if 0 <= coord[0] <= self.size - 1 and 0 <= coord[0] <= self.size - 1:
                if not self.board[coord[0]][coord[1]]:
                    return coord
        return None

    def count_liberty(self, coord):
        neigh_points = self.find_neigh_points(coord)
        i = 0
        while i < len(neigh_points):
            if self.board[neigh_points[i][0]][neigh_points[i][1]]:
                neigh_points.pop(i)
            else:
                i += 1
        return len(neigh_points)

    def change_liberty(self, coord, sign):
        neigh_points = self.find_neigh_points(coord)
        for point in neigh_points:
            if self.board[point[0]][point[1]]:
                if sign == '-':
                    self.board[point[0]][point[1]].liberty -= 1
                else:
                    self.board[point[0]][point[1]].liberty += 1

    def find_neigh_points(self, coord):
        neigh_points = [(coord[0], coord[1] - 1),
                        (coord[0] - 1, coord[1]),
                        (coord[0], coord[1] + 1),
                        (coord[0] + 1, coord[1])]
        i = 0
        while i < len(neigh_points):
            if 0 <= neigh_points[i][0] <= self.size - 1 and 0 <= neigh_points[i][1] <= self.size - 1:
                i += 1
            else:
                neigh_points.pop(i)
        return neigh_points

    def find_winner(self):
        pass


class Stone:

    def __init__(self, liberty):
        self.liberty = liberty


class BlackStone(Stone):

    def __init__(self, liberty):
        Stone.__init__(self, liberty)


class WhiteStone(Stone):

    def __init__(self, liberty):
        Stone.__init__(self, liberty)
