import pygame
from circleshape import CircleShape
from constants import (
    POWERUP_PIERCE_COLOUR,
    POWERUP_RADIUS,
    POWERUP_SPEEDSHOT_COLOUR,
    POWERUP_MULTISHOT_COLOUR,
    POWERUP_SHIELD_COLOUR
)
from enum import Enum
import random

class PowerupType(Enum):
    PIERCE = 1
    SPEEDSHOT = 2
    MULTISHOT = 3
    SHIELD = 4

class Powerup(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, POWERUP_RADIUS)
        self.colour = "white"
        self.type = None
        self.generate_type()
        
    def draw(self, screen):
        pygame.draw.circle(surface=screen, color=self.colour, center = self.position, radius = self.radius, width=2)
        
    def generate_type(self):
        self.type = random.choice(list(PowerupType))
        match(self.type):
            case PowerupType.PIERCE:
                self.colour = POWERUP_PIERCE_COLOUR
            case PowerupType.SPEEDSHOT:
                self.colour = POWERUP_SPEEDSHOT_COLOUR
            case PowerupType.MULTISHOT:
                self.colour = POWERUP_MULTISHOT_COLOUR
            case PowerupType.SHIELD:
                self.colour = POWERUP_SHIELD_COLOUR
