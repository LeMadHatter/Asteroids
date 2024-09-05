import pygame
from player import *
from constants import *
from asteroids import *
from asteroidfield import *
from shot import *
import sys

def main():
    print("Starting asteroids!")
    pygame.init()
    game_clock = pygame.time.Clock()
    dt = 0
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)
    
    while True:
        pygame.display.flip()
        screen.fill("#000000")
        
        for item in updatable:
            item.update(dt)
        for asteroid in asteroids:
            if asteroid.is_colliding(player) and not player.invicibility:
                sys.exit("GAME OVER NOOB!")
            for shot in shots:
                if asteroid.is_colliding(shot):
                    asteroid.split()
                    shot.kill()
        for item in drawable:
            item.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        dt = game_clock.tick(60) / 1000


if __name__ == "__main__":
    main()