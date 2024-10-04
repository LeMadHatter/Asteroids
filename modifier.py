import pygame
from constants import *

class Modifier(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.type = type
        self.position = pygame.Vector2(x, y)
        self.width = 18
        self.font = pygame.font.SysFont('Comic Sans MS', 15)

    def draw(self, screen):
        pygame.draw.rect(screen, MODIFIER_COLORS[self.type], self.rectangle(), 0)
        text = self.font.render(f"{self.type}", True,  MODIFIER_COLORS[self.type])
        screen.blit(text, (self.position.x - 20, self.position.y + 22))

    def rectangle(self):
        return [self.position.x, self.position.y, self.width, self.width]
    
    def is_colliding(self, other_circle):
        distance = pygame.math.Vector2.distance_to(self.position, other_circle.position)
        return distance <= self.width + other_circle.radius