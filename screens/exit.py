import pygame
from widgets import Notification
from language import lang


pygame.init()


def exit(display):
    notification = Notification(display, lang.data["exit game"])
    notification.run()
    if notification.action:
        pygame.quit()
        quit()
    del notification
