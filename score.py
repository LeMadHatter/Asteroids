import pygame

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.current_score = 0
        self.color = '#FFFFFF'
    
    def draw(self, screen):
        button_text = self.font.render(f"Score : {self.current_score}", True, self.color)
        screen.blit(button_text, (0, 0))

    def update(self, points_to_add):
        self.current_score += points_to_add