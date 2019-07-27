import pygame
from settings import color, display_size, FPS


pygame.init()
clock = pygame.time.Clock()


class Button:

    def __init__(self, name, size, pos):
        self.name = name
        self.size = size
        self.pos = pos
        self.is_pressed = False
        self.is_click = False
        self.active = False

    def draw(self, surface):
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


class Notification:

    def __init__(self, surface, text):
        self.surface = surface
        self.text = text
        self.btn_yes = Button('yes', [140, 50], [260, 300])
        self.btn_no = Button('no', [140, 50], [500, 300])
        self.show = True
        self.action = False

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.draw.rect(self.surface, color['green'], 
                         (0, 150, display_size[0], 300))
        font = pygame.font.Font(None, 50)
        text = font.render(self.text, 1, color['white'])
        lb = text.get_rect(center = (display_size[0]/2, 200))
        self.surface.blit(text, lb)
        self.btn_yes.draw(self.surface)
        self.btn_no.draw(self.surface)
        if self.btn_no.active:
            self.show = False
        elif self.btn_yes.active:
            self.show = False
            self.action = True
            

    def run(self):
        while self.show:
            self.draw()
            pygame.display.update()
            clock.tick(FPS)