import pygame
from circleshape import CircleShape
from constants import (
    LASER_COLOUR,
    LASER_SPEED,
    LASER_RADIUS
)

class Laser(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, LASER_RADIUS)

    def fire(self, rotation):
        self.velocity = pygame.Vector2(0,1).rotate(rotation) * LASER_SPEED
        
    def draw(self, screen):
        pygame.draw.circle(surface=screen, color=LASER_COLOUR, center = self.position, radius = self.radius, width=2)
        
    def update(self, dt):
        self.position += (self.velocity * dt)