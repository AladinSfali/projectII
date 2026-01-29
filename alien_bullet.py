import pygame
import math
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """A class to manage bullets fired from aliens."""

    def __init__(self, ai_game, alien):
        """Create a bullet object at the alien's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien laser image.
        try:
            self.image = pygame.image.load('images/missile.png')
        except FileNotFoundError:
            # Fallback if image is missing
            self.image = pygame.Surface((self.settings.bullet_width, self.settings.bullet_height))
            self.image.fill((255, 0, 0))

        # Calculate angle to the ship
        ship = ai_game.ship
        dx = ship.rect.centerx - alien.rect.centerx
        dy = ship.rect.centery - alien.rect.centery
        angle = math.atan2(dy, dx)
        
        # Rotate the image to point towards the ship (assuming missile points UP by default)
        self.image = pygame.transform.rotate(self.image, -math.degrees(angle) - 90)

        self.rect = self.image.get_rect()
        self.rect.center = alien.rect.center
        
        # Store the bullet's position and velocity.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.x_speed = math.cos(angle) * self.settings.alien_bullet_speed
        self.y_speed = math.sin(angle) * self.settings.alien_bullet_speed

    def update(self):
        """Move the bullet towards the target."""
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)