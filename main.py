import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from laser import Laser

def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Laser.containers = (updatable, drawable, lasers)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(x = SCREEN_WIDTH/2, y = SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill(color = "black")
        for update_object in updatable:
            update_object.update(dt)
        for draw_object in drawable:
            draw_object.draw(screen)
        for asteroid in asteroids:
            if asteroid.check_for_collision(player):
                print("GAME OVER!")
                return
            for laser in lasers:
                if asteroid.check_for_collision(laser):
                    asteroid.split()
                    laser.kill()
        pygame.display.flip()
        dt = (clock.tick(FPS))/1000

if __name__ == "__main__":
    main()