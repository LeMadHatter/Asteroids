import pygame, sys
from constants import *


class Button(pygame.sprite.Sprite):
    def __init__(self, text, text_color, bottom_left_corner_x, bottom_left_corner_y, border_width, border_color = "#FFFFFF", fade_timer = float('inf')):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.text = text
        self.pos = pygame.Vector2(bottom_left_corner_x, bottom_left_corner_y)
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.fade_timer = fade_timer
        self.text_color = text_color
        self.border_width = border_width
        self.border_color = border_color


    def rectangle(self):
        return [self.pos.x, self.pos.y, self.width, self.height]
    
    def draw(self, screen):
        if self.fade_timer > 0:
            pygame.draw.rect(screen, self.border_color, self.rectangle(), self.border_width)
            button_text = self.font.render(self.text, True, self.text_color)
            screen.blit(button_text, (self.pos.x + BUTTON_WIDTH / 10, self.pos.y + BUTTON_HEIGHT / 3))
            self.needs_draw_text = False

    def update(self, dt):
        self.fade_timer -= dt

    def is_clicked(self, input_pos): #input_pos must be pygame vertex2
        
        return (input_pos.x >= self.pos.x 
        and input_pos.x <= self.pos.x + BUTTON_WIDTH
        and input_pos.y >= self.pos.y
        and input_pos.y <= self.pos.y + BUTTON_HEIGHT
        and pygame.mouse.get_pressed()[0])