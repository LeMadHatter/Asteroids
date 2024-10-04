import pygame
from player import *
from constants import *
from asteroids import *
from asteroidfield import *
from shot import *
from menu import *
from modifier import *
import sys
import os



def main():
    print("Starting asteroids!")
    pygame.init()

    game_state = "Start Menu"
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_clock = pygame.time.Clock()
    dt = 0
    

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    modifiers = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Button.containers = (menu, updatable, drawable)
    Modifier.containers = (updatable, drawable, modifiers)

    asteroid_field = AsteroidField()
    new_game_button = Button('New Game', "#FFFFFF", SCREEN_WIDTH / 8, SCREEN_HEIGHT / 6, 2)
    quit_button = Button('Quit', "#FFFFFF", SCREEN_WIDTH / 8, SCREEN_HEIGHT / 6 + BUTTON_SPACING, 2)
    game_over_button = Button('Game Over!', (255, 0, 0), SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, SCREEN_HEIGHT / 2 - BUTTON_HEIGHT / 2, 0, "#000000", float('-inf'))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)
    
    while True:
        pygame.display.flip()
        screen.fill("#000000")

        if len(modifiers.sprites()) > AVAILABLE_MODIFIERS_LIMIT:
            modifiers.sprites()[0].kill()

        if new_game_button.is_clicked(pygame.Vector2(pygame.mouse.get_pos())):
            player.reset_player()
            game_state = "Game"
            for item in asteroids:
                item.kill()

        if quit_button.is_clicked(pygame.Vector2(pygame.mouse.get_pos())):
            sys.exit()

        if game_state == "Start Menu":
            player.invicibility = True

        for asteroid in asteroids:
            if asteroid.is_colliding(player) and not player.invicibility:
                player.lose_life(dt)
                if player.extra_lives == 0:
                    if game_state == "Game":
                        game_over_button.fade_timer = 3
                    game_state = "Game Over"


            for shot in shots:
                if asteroid.is_colliding(shot):
                    asteroid.split()
                    if not player.active_modifier == "Piercing shot":
                        shot.kill()
                    if game_state == "Game":
                        player.score.update(10)

        for modifier in modifiers:
            if modifier.is_colliding(player):
                player.active_modifier = modifier.type
                player.modifier_timer = MODIFIER_TIMER[modifier.type]
                modifier.kill()

        for item in updatable:
            if game_over_button.fade_timer < 0 and game_state == "Game Over":
                game_state = "Start Menu"
                player.reset_player()
                player.invicibility = True
                for item in asteroids:
                    item.kill()


            if game_state == "Game":
                if item not in menu:
                    item.update(dt)
            elif game_state == "Game Over":
                if item in menu:
                    item.update(dt)
            else:
                item.update(dt)

        for item in drawable:
            if game_state == "Game":
                if item not in menu:
                    item.draw(screen)
            else:
                item.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        dt = game_clock.tick(60) / 1000



    #https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    main()