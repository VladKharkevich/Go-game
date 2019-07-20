import pygame


pygame.init()
display_size = (800, 600)
display = pygame.display.set_mode(display_size)
pygame.display.set_caption('GO')
clock = pygame.time.Clock()
turn = True
color = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'brown': (0xcd, 0x85, 0x3f)
}


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
        display.fill(color['white'])
        draw_board(go_board)
        font = pygame.font.Font(None, 72)
        if turn:
            text = font.render("Black's turn", 1, (0, 100, 0))
        else:
            text = font.render("White's turn", 1, (0, 100, 0))
        place = text.get_rect(center=(400, 50))
        display.blit(text, place)
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            make_step(go_board)
        pygame.display.update()
        clock.tick(60)


def draw_board(go_board):
    pygame.draw.rect(display, color['brown'],
                     (150, 80, 30 + 18 * 25, 30 + 18 * 25))
    for i in range(19):
        pygame.draw.line(display, color['black'],
                         (165 + 25 * i, 95), (165 + 25 * i, 545), 3)
        pygame.draw.line(display, color['black'],
                         (165, 95 + 25 * i), (615, 95 + 25 * i), 3)
    for i in range(19):
        for j in range(19):
            if go_board.board[i][j] == 'black':
                pygame.draw.circle(display, color['black'],
                                   (165 + 25 * i, 95 + 25 * j), 12)
            elif go_board.board[i][j] == 'white':
                pygame.draw.circle(display, color['white'],
                                   (165 + 25 * i, 95 + 25 * j), 12)


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
    if (pos[0] in range(160, 621)) and (pos[1] in range(90, 551)) and (
            pos[0] % 25 > 10 or pos[0] % 25 < 20) and (pos[1] % 25 > 15):
        coord = [(pos[0] - 160) // 25, (pos[1] - 90) // 25]
        if go_board.board[coord[0]][coord[1]] == 'blank':
            return coord
    return None


rungame()
