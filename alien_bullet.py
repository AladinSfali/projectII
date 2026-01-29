import pygame
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

        self.rect = self.image.get_rect()
        self.rect.midbottom = alien.rect.midbottom
        
        # Store the bullet's position as a float.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet down the screen."""
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)