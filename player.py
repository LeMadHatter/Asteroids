from circleshape import *
from constants import *
from shot import *
from score import *
import sys

class Player(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.shot_timer = 0
        self.key_timer = 0
        self.invicibility = True
        self.extra_lives = BASE_EXTRA_LIVES
        self.lost_life = False
        self.lose_life_timer = 2
        self.flash_timer = 0.5
        self.color = "#FFFFFF"
        self.update_extra_lives = True
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.score = Score()

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.triangle(), 2)
        self.score.draw(screen)
        if self.update_extra_lives:
            button_text = self.font.render(f"Extra lives : {self.extra_lives}", True, self.color)
            screen.blit(button_text, (0, 30))
        
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        self.rotation = self.rotation % 360

    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt, keys[pygame.K_LCTRL])
        if keys[pygame.K_s]:
            self.move(-dt, keys[pygame.K_LCTRL])
        if keys[pygame.K_r]:
            self.reset_pos()
        if keys[pygame.K_ESCAPE]:
            sys.exit("Game closed by human")
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_i]:
            if self.key_timer > 0:
                return
            self.invicibility = not self.invicibility
            print(f"Invicible : {self.invicibility}")
            self.key_timer = KEY_COOLDOWN
        
        if self.lost_life:
            self.lose_life(dt)

        self.key_timer -= dt
        self.shot_timer -= dt
        

    def move(self, dt, sprint):
        if not self.lost_life:
            if sprint:
                dt *= 5
            forward = pygame.Vector2(0, 1).rotate(self.rotation)

            if (self.position.x + forward.x * PLAYER_SPEED * dt > SCREEN_WIDTH 
                or self.position.x + forward.x * PLAYER_SPEED * dt < 0):
                forward = pygame.Vector2(0, pygame.Vector2(0, 1).rotate(self.rotation).y)

            if (self.position.y + forward.y * PLAYER_SPEED * dt > SCREEN_HEIGHT
                or self.position.y + forward.y * PLAYER_SPEED * dt < 0):
                forward = pygame.Vector2(pygame.Vector2(0,1).rotate(self.rotation).x, 0)      

            if (self.position.x + forward.x * PLAYER_SPEED * dt > SCREEN_WIDTH 
                or self.position.x + forward.x * PLAYER_SPEED * dt < 0):
                forward.x = 0

            if (self.position.y + forward.y * PLAYER_SPEED * dt > SCREEN_HEIGHT
                or self.position.y + forward.y * PLAYER_SPEED * dt < 0):
                forward.y = 0

            self.position += forward * PLAYER_SPEED * dt
    

    def shoot(self):
        if not self.lost_life:
            if self.shot_timer > 0:
                return
            self.shot_timer = PLAYER_SHOOT_COOLDOWN
            new_shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            new_shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        
    def reset_player(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.rotation = 0
        self.invicibility = False
        self.extra_lives = BASE_EXTRA_LIVES
        self.lose_life_timer = 2
        self.lost_life = False
        self.color = "#FFFFFF"
        self.score.current_score = 0

    def lose_life(self, dt):
        self.lose_life_timer -= dt
        self.flash_timer -= dt
        self.lost_life = True
        self.invicibility = True
        
        if self.flash_timer < 0:
            if self.color == "#FFFFFF":
                self.color = (255,0,0)
            else:
                self.color = "#FFFFFF"
            self.flash_timer = 0.3

        if self.lose_life_timer < 0:
            self.lose_life_timer = 2
            self.lost_life = False
            self.invicibility = False
            self.color = "#FFFFFF"
        if not self.lost_life:
            self.extra_lives -= 1