import pygame
from pygame.sprite import Sprite

class PowerUp(Sprite):
    """A class to manage power-ups dropped by aliens."""

    def __init__(self, ai_game, center):
        """Create a power-up object at the alien's position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the power-up image.
        try:
            self.image = pygame.image.load('images/powerup_bolt.png')
        except FileNotFoundError:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 215, 0)) # Gold color

        self.rect = self.image.get_rect()
        self.rect.center = center
        
        self.y = float(self.rect.y)

    def update(self):
        """Move the power-up down the screen."""
        self.y += 1.5 
        self.rect.y = self.y