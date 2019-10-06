import pygame
import os
from settings import color


pygame.init()


class Board:

    def __init__(self, size):
        self.size = size
        self.board = [[None for i in range(size)] for j in range(size)]
        self.list_of_turns = []
        self.turn = True

    def draw(self, surface):
        pygame.draw.rect(surface, color['brown'],
                         (150, 80, 30 + 18 * 25, 30 + 18 * 25))
        for i in range(self.size):
            pygame.draw.line(surface, color['black'],
                             (165 + 25 * i, 95), (165 + 25 * i, 545), 3)
            pygame.draw.line(surface, color['black'],
                             (165, 95 + 25 * i), (615, 95 + 25 * i), 3)
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j]:
                    surface.blit(self.board[i][j].image,
                                 (152 + 25 * i, 82 + 25 * j))

    def make_step(self):
        pos = pygame.mouse.get_pos()
        coord = self.find_coordinates(pos)
        if coord:
            liberty = self.count_liberty(coord)
            if liberty[0] > 0:
                if self.turn:
                    self.board[coord[0]][coord[1]] = BlackStone(liberty[1])
                else:
                    self.board[coord[0]][coord[1]] = WhiteStone(liberty[1])
                self.degree_liberty(coord)
                neigh_points = self.find_neigh_points(coord)
                for point in neigh_points:
                    if type(self.board[point[0]][point[1]]) != type(self.board[coord[0]][coord[1]]):
                        self.temp = []
                        if not self.stone_is_alive(point):
                            for elem in self.temp:
                                self.board[elem[0]][elem[1]] = None
                self.list_of_turns.append(coord)
                self.turn = not self.turn

    def stone_is_alive(self, coord):
        if self.count_liberty(coord)[1] == 0:
            self.temp.append(coord)
            neigh_points = self.find_neigh_points(coord)
            for point in neigh_points:
                if (point not in self.temp) and (type(self.board[point[0]][point[1]]) == type(self.board[coord[0]][coord[1]])):
                    if self.stone_is_alive(point):
                        return True
        else:
            return True

    def find_coordinates(self, pos):
        if (pos[0] in range(160, 621)) and (pos[1] in range(90, 551)) and (
                pos[0] % 25 > 10 or pos[0] % 25 < 20) and (pos[1] % 25 > 15):
            coord = [(pos[0] - 160) // 25, (pos[1] - 90) // 25]
            if not self.board[coord[0]][coord[1]]:
                return coord
        return None

    def count_liberty(self, coord):
        our_side = BlackStone
        enemy_side = WhiteStone
        if not self.turn:
            our_side, enemy_side = enemy_side, our_side
        neigh_points = self.find_neigh_points(coord)
        i = 0
        while i < len(neigh_points):
            if type(self.board[neigh_points[i][0]][neigh_points[i][1]]) is enemy_side:
                neigh_points.pop(i)
            else:
                i += 1
        positive_liberty = len(neigh_points)
        i = 0
        while i < len(neigh_points):
            if type(self.board[neigh_points[i][0]][neigh_points[i][1]]) is our_side:
                neigh_points.pop(i)
            else:
                i += 1
        free_liberty = len(neigh_points)
        return positive_liberty, free_liberty

    def degree_liberty(self, coord):
        neigh_points = self.find_neigh_points(coord)
        for point in neigh_points:
            if self.board[point[0]][point[1]]:
                self.board[point[0]][point[1]].liberty -= 1

    @staticmethod
    def find_neigh_points(coord):
        neigh_points = [(coord[0], coord[1] - 1),
                        (coord[0] - 1, coord[1]),
                        (coord[0], coord[1] + 1),
                        (coord[0] + 1, coord[1])]
        i = 0
        while i < len(neigh_points):
            if 0 <= neigh_points[i][0] <= 18 and 0 <= neigh_points[i][1] <= 18:
                i += 1
            else:
                neigh_points.pop(i)
        return neigh_points


class Stone:

    def __init__(self, liberty):
        self.liberty = liberty


class BlackStone(Stone):

    def __init__(self, liberty):
        Stone.__init__(self, liberty)
        image = pygame.image.load(os.path.join('images/black.png'))
        self.image = pygame.transform.scale(image,
                                            (image.get_width() // 4,
                                             image.get_height() // 4))


class WhiteStone(Stone):

    def __init__(self, liberty):
        Stone.__init__(self, liberty)
        image = pygame.image.load(os.path.join('images/white.png'))
        self.image = pygame.transform.scale(image,
                                            (image.get_width() // 4,
                                             image.get_height() // 4))
