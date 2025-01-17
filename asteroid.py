import pygame
from circleshape import CircleShape
from constants import (
    ASTEROID_COLOUR,
    ASTEROID_MIN_RADIUS,
    ASTEROID_MAX_RADIUS,
    ASTEROID_SPEED_BOOST,
    POWERUP_CHANCE
    )
import random
from powerup import Powerup

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        pygame.draw.circle(surface=screen, color=ASTEROID_COLOUR, center = self.position, radius = self.radius, width=2)
        
    def update(self, dt):
        self.position += (self.velocity * dt)
        
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        # Calculate powerup drop chance proportionally
        proportional_chance = POWERUP_CHANCE * (self.radius / ASTEROID_MAX_RADIUS) ** 3
        if random.randint(1, 100) <= proportional_chance:
            powerup = Powerup(self.position.x, self.position.y)
            
        angle = random.uniform(20, 50)
        vec1 = self.velocity.rotate(angle)
        vec2 = self.velocity.rotate(-angle)
        new_rad = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_rad)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_rad)
        asteroid1.velocity = vec1 * ASTEROID_SPEED_BOOST
        asteroid2.velocity = vec2 * ASTEROID_SPEED_BOOST
        
    