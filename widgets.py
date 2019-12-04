import pygame
from settings import color, display_size, FPS
from language import lang

pygame.init()
clock = pygame.time.Clock()


class Button:

    def __init__(self, name, size, pos, font_size=54):
        self.name = name
        self.size = size
        self.pos = pos
        self.font_size = font_size
        self.is_pressed = False
        self.is_click = False
        self.active = False
        self.key_name = self.get_key_name()

    def draw(self, surface):
        if (not pygame.mouse.get_pressed()[0] and self.is_pressed and
                self.mouse_on_button()):
            self.active = True
        if self.key_name:
            self.name = lang.data[self.key_name]
        self.click_button()
        if self.mouse_on_button() and self.is_pressed:
            pygame.draw.rect(surface, color['green'], (self.pos[0],
                                                       self.pos[1], self.size[0], self.size[1]))
        else:
            pygame.draw.rect(surface, color['brown'], (self.pos[0],
                                                       self.pos[1], self.size[0], self.size[1]))
        font = pygame.font.Font(None, self.font_size)
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
        if (self.pos[0] <= pygame.mouse.get_pos()[0] <= self.pos[0] +
            self.size[0]) and (self.pos[1] <= pygame.mouse.get_pos()[1] <=
                               self.pos[1] + self.size[1]):
            return True
        return False

    def get_key_name(self):
        for key, value in lang.data.items():
            if value == self.name:
                return key


class Notification:

    def __init__(self, surface, text):
        self.surface = surface
        self.text = text
        self.btn_yes = Button(lang.data["yes"], [140, 50], [260, 300])
        self.btn_no = Button(lang.data["no"], [140, 50], [500, 300])
        self.show = True
        self.action = False

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.show = False
                    self.action = True
                elif event.key == pygame.K_ESCAPE:
                    self.show = False
        pygame.draw.rect(self.surface, color['green'],
                         (0, 150, display_size[0], 300))
        font = pygame.font.Font(None, 50)
        text = font.render(self.text, 1, color['white'])
        lb = text.get_rect(center=(display_size[0] / 2, 200))
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


class Toggle:

    def __init__(self, pos):
        self.pos = pos
        self.is_pressed = False
        self.is_click = False
        self.active = False
        self.size = [60, 30]

    def draw(self, surface):
        if (not pygame.mouse.get_pressed()[0] and self.is_pressed and
                self.mouse_on_toggle()):
            self.active = not self.active
        self.click_toggle()
        if self.active:
            color_of_toggle = color['pink']
        else:
            color_of_toggle = color['sky-blue']
        pygame.draw.circle(surface, color_of_toggle, (self.pos[0],
                                                      self.pos[1] + int(self.size[1] / 2)),
                           int(self.size[1] / 2))
        pygame.draw.circle(surface, color_of_toggle, (self.pos[0] + self.size[0],
                                                      self.pos[1] + int(self.size[1] / 2)),
                           int(self.size[1] / 2))
        pygame.draw.rect(surface, color_of_toggle, (self.pos[0],
                                                    self.pos[1], self.size[0], self.size[1]))
        if self.active:
            pygame.draw.circle(surface, color['white'], (self.pos[0] + self.size[0],
                                                         self.pos[1] + int(self.size[1] / 2)),
                               int(self.size[1] / 2 - 3))
        else:
            pygame.draw.circle(surface, color['white'], (self.pos[0],
                                                         self.pos[1] + int(self.size[1] / 2)),
                               int(self.size[1] / 2 - 3))

    def click_toggle(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.is_click:
                self.is_click = True
                if self.mouse_on_toggle():
                    self.is_pressed = True
        else:
            self.is_click = False
            self.is_pressed = False

    def mouse_on_toggle(self):
        if (self.pos[0] <= pygame.mouse.get_pos()[0] <= self.pos[0] +
            self.size[0]) and (self.pos[1] <= pygame.mouse.get_pos()[1] <=
                               self.pos[1] + self.size[1]) or ((pygame.mouse.get_pos()[0] -
                                                                self.pos[0])**2 + (pygame.mouse.get_pos()[1] - (self.pos[1] + self.size[1] / 2))**2 <= (self.size[1] / 2)**2) or (
            (pygame.mouse.get_pos()[0] - (self.pos[0] + self.size[0]))**2
            + (pygame.mouse.get_pos()[1] - (self.pos[1] + self.size[1] /
                                            2))**2 <= (self.size[1] / 2)**2):
            return True
        return False


class MessageBox:

    def __init__(self, surface, text):
        self.surface = surface
        self.text = text
        self.btn_ok = Button(lang.data["ok"], [140, 50], [380, 300])
        self.show = True

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.draw.rect(self.surface, color['green'],
                         (120, 150, 660, 300))
        font = pygame.font.Font(None, 50)
        text = font.render(self.text, 1, color['white'])
        lb = text.get_rect(center=(display_size[0] / 2, 200))
        self.surface.blit(text, lb)
        self.btn_ok.draw(self.surface)
        if self.btn_ok.active:
            self.show = False

    def run(self):
        while self.show:
            self.draw()
            pygame.display.update()
            clock.tick(FPS)


class Slider:

    def __init__(self):
        self.pos_rect_y = 15
        self.value = 0
        self.btn_active = False
        self.is_draw = False

    def draw(self, surface):
        pygame.draw.rect(surface, color['gray'], (830, 40, 20, 500))
        if pygame.mouse.get_pressed()[0]:
            if (830 <= pygame.mouse.get_pos()[0] <= 850) and (
                    40 <= pygame.mouse.get_pos()[1] <= 540):
                pygame.draw.rect(
                    surface, color['light-green'], (825, self.pos_rect_y, 30, 50))
                self.pos_rect_y = pygame.mouse.get_pos()[1] - 25
                self.value = round((self.pos_rect_y - 15) / 5)
                self.is_draw = True
            elif (825 <= pygame.mouse.get_pos()[0] <= 855) and (
                    self.pos_rect_y <= pygame.mouse.get_pos()[1] <= self.pos_rect_y + 50):
                pygame.draw.rect(
                    surface, color['light-green'], (825, self.pos_rect_y, 30, 50))
                self.btn_active = True
                self.value = round((self.pos_rect_y - 15) / 5)
                self.is_draw = True
            elif self.btn_active:
                pygame.draw.rect(
                    surface, color['light-green'], (825, self.pos_rect_y, 30, 50))
                self.is_draw = True
                if (40 <= pygame.mouse.get_pos()[1] <= 540):
                    self.pos_rect_y = pygame.mouse.get_pos()[1] - 25
                    self.value = round((self.pos_rect_y - 15) / 5)
        if not self.is_draw:
            pygame.draw.rect(
                surface, color['green'], (825, self.pos_rect_y, 30, 50))
            self.btn_active = False
        self.is_draw = False
