from circleshape import *
from constants import *
from shot import *
import sys

class Player(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.shot_timer = 0
        self.key_timer = 0
        self.invicibility = True

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "#FFFFFF", self.triangle(), 2)

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
            self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
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

        self.key_timer -= dt
        self.shot_timer -= dt

    def move(self, dt, sprint):
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
        if self.shot_timer > 0:
            return
        self.shot_timer = PLAYER_SHOOT_COOLDOWN
        new_shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        new_shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        