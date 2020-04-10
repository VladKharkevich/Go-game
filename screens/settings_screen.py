import pygame
from settings import color, sound
from widgets import Button, Toggle
from language import lang

from .main_screen import MainScreen
from .rools_screen import Rools
from .about_program_screen import AboutProgram


pygame.init()


class Settings(MainScreen):

    def __init__(self, display):
        MainScreen.__init__(self, display)
        self.btn_about_program = Button(
            lang.data["program"], [240, 50], [340, 270], 38)
        self.btn_rools = Button(lang.data["rools"], [240, 50], [340, 340], 38)
        self.btn_main_menu = Button(lang.data["main menu"], [
                                    240, 50], [340, 410], 38)
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
