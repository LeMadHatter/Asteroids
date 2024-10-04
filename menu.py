import pygame
from constants import *
from button import Button

class Menu():
    def __init__(self, screen, shown = True):
        self.screen = screen
        # self.new_game = Button('New Game', SCREEN_WIDTH / 8, SCREEN_HEIGHT / 6, "New game")
        # self.quit = Button('Quit', SCREEN_WIDTH / 8, SCREEN_HEIGHT / 6 + BUTTON_SPACING, 'Quit')
        self.buttons = [self.new_game, self.quit]


    def display_menu(self, screen):
        while True:
            for button in self.buttons:
                button.draw(screen)
