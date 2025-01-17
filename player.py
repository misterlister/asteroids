import pygame
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_COLOUR,
    PLAYER_SHOT_BASE_SPEED,
    POWERUP_SPEEDSHOT_FACTOR,
    POWERUP_DURATION,
    POWERUP_MULTISHOT_ANGLE,
    POWERUP_SHIELD_COLOUR,
    SHIELD_DURATION,
    PROTECTED_COLOUR
)
from laser import Laser
from powerup import Powerup, PowerupType

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_timer = 0
        self.shot_speed = PLAYER_SHOT_BASE_SPEED
        self.pierce_timer = 0
        self.multishot_timer = 0
        self.multishot_stacks = 0
        self.speed_shot_timer = 0
        self.colour = PLAYER_COLOUR
        self.shield = False
        self.shield_timer = 0
        
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, self.colour, self.triangle(), width=2)
    
    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)
        
    def update(self, dt):
        keys = pygame.key.get_pressed()

        self.shot_timer -= dt
        self.update_powerups(dt)
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.shot_timer <= 0:
                self.shoot()
            
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        
    def shoot(self):
        # Fire the main shot
        main_shot = Laser(self.position.x, self.position.y)
        main_shot.fire(self.rotation)

        # Fire additional shots for each multishot stack
        for stack in range(1, self.multishot_stacks + 1):
            # Calculate the angles for each stack
            left_angle = self.rotation - (stack * POWERUP_MULTISHOT_ANGLE)
            right_angle = self.rotation + (stack * POWERUP_MULTISHOT_ANGLE)

            # Fire the left shot
            left_shot = Laser(self.position.x, self.position.y)
            left_shot.fire(left_angle)

            # Fire the right shot
            right_shot = Laser(self.position.x, self.position.y)
            right_shot.fire(right_angle)

        # Reset the shot timer
        self.shot_timer = self.shot_speed
        
    def update_powerups(self, dt):
        if self.pierce_timer > 0:
            self.pierce_timer -= dt
        if self.multishot_timer > 0:
            self.multishot_timer -= dt
            if self.multishot_timer <= 0:
                self.multishot_stacks = 0
        if self.speed_shot_timer > 0:
            self.speed_shot_timer -= dt
            if self.speed_shot_timer <= 0:
                self.shot_speed = PLAYER_SHOT_BASE_SPEED
        if self.shield_timer > 0:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.colour = PLAYER_COLOUR
        
    def get_powerup(self, powerup: Powerup):
        match (powerup.type):
            case PowerupType.SPEEDSHOT:
                self.shot_speed *= POWERUP_SPEEDSHOT_FACTOR
                self.speed_shot_timer = POWERUP_DURATION
            case PowerupType.PIERCE:
                self.pierce_timer = POWERUP_DURATION
            case PowerupType.MULTISHOT:
                self.multishot_timer = POWERUP_DURATION
                self.multishot_stacks += 1
            case PowerupType.SHIELD:
                self.get_shield()
        powerup.kill()
        
    def multishot_powerup(self):
        return self.multishot_timer > 0
    
    def pierce_powerup(self):
        return self.pierce_timer > 0
    
    def shielded(self):
        if self.shield:
            return True
        return False
    
    def protected(self):
        if self.shield_timer > 0:
            return True
        return False
    
    def get_shield(self):
        self.shield = True
        self.colour = POWERUP_SHIELD_COLOUR
        
    def break_shield(self):
        self.shield = False
        self.colour = PROTECTED_COLOUR
        self.shield_timer = SHIELD_DURATION