import pygame
from settings import display_size, color
from game import Board, ButtonPass


pygame.init()
display = pygame.display.set_mode(display_size)
pygame.display.set_caption('GO')
clock = pygame.time.Clock()


def rungame():
    go_board = Board(19)
    game = True
    btn_pass = ButtonPass('pass', [150, 70], [700, 300])
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                go_board.make_step()
        display.fill(color['white'])
        go_board.draw_board(display)
        btn_pass.draw_button(display)
        if btn_pass.action:
            btn_pass.btn_function(go_board)
        font = pygame.font.Font(None, 72)
        if go_board.turn:
            text = font.render("Black's turn", 1, color['green'])
        else:
            text = font.render("White's turn", 1, color['green'])
        lbturn = text.get_rect(center=(400, 50))
        display.blit(text, lbturn)
        pygame.display.update()
        clock.tick(60)


rungame()
