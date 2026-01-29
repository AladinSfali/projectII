import pygame
import math
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the bullet image and rotate it to match the ship's angle.
        try:
            self.image = pygame.image.load('images/missile.png')
            self.image = pygame.transform.scale(self.image, (self.settings.bullet_width, self.settings.bullet_height))
        except FileNotFoundError:
            self.image = pygame.Surface((self.settings.bullet_width, self.settings.bullet_height))
            self.image.fill(self.settings.bullet_color)

        self.angle = ai_game.ship.angle
        self.image = pygame.transform.rotate(self.image, self.angle)
        
        # Set the rect and its position.
        self.rect = self.image.get_rect()
        self.rect.center = ai_game.ship.rect.center
    
        # Store the bullet's position and trajectory.
        angle_rad = math.radians(self.angle)
        
        # Calculate speed components based on the ship's angle.
        self.x_speed = -self.settings.bullet_speed * math.sin(angle_rad)
        self.y_speed = -self.settings.bullet_speed * math.cos(angle_rad)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet in the direction it was fired."""
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.image, self.rect)