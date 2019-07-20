import pygame


pygame.init()
display_size = (800, 600)
display = pygame.display.set_mode(display_size)
pygame.display.set_caption('GO')
clock = pygame.time.Clock()
make_jump = False
turn = True


class Board:

    def __init__(self, size):
        self.size = size
        self.board = [['blank' for i in range(size)] for j in range(size)]


def rungame():
    go_board = Board(19)
    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.fill((255, 255, 255))
        draw_board(go_board)
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            make_step(go_board)
        pygame.display.update()
        clock.tick(60)


def draw_board(go_board):
    pygame.draw.rect(display, (0xcd, 0x85, 0x3f),
                     (150, 50, 30 + 18 * 25, 30 + 18 * 25))
    for i in range(19):
        pygame.draw.line(display, (0, 0, 0),
                         (165 + 25 * i, 65), (165 + 25 * i, 515), 3)
        pygame.draw.line(display, (0, 0, 0),
                         (165, 65 + 25 * i), (615, 65 + 25 * i), 3)
    for i in range(19):
        for j in range(19):
            if go_board.board[i][j] == 'black':
                pygame.draw.circle(display, (0, 0, 0),
                                   (165 + 25 * i, 65 + 25 * j), 12)
            elif go_board.board[i][j] == 'white':
                pygame.draw.circle(display, (255, 255, 255),
                                   (165 + 25 * i, 65 + 25 * j), 12)


def make_step(go_board):
    global turn
    pos = pygame.mouse.get_pos()
    coord = find_coordinates(pos, go_board)
    if coord:
        if turn:
            go_board.board[coord[0]][coord[1]] = 'black'
        else:
            go_board.board[coord[0]][coord[1]] = 'white'
        turn = not turn


def find_coordinates(pos, go_board):
    if (pos[0] in range(160, 621)) and (pos[1] in range(60, 521)) and (
            pos[0] % 25 > 10 or pos[0] % 25 < 20) and (
            pos[1] % 25 > 10 or pos[1] % 25 < 20):
        coord = [(pos[0] - 160) // 25, (pos[1] - 60) // 25]
        if go_board.board[coord[0]][coord[1]] == 'blank':
            return coord
    return None


rungame()