import pygame
from pygame.sprite import Sprite
import random

class Star(Sprite):
    """A class to represent a single star in the background."""

    def __init__(self, ai_game):
        """Initialize the star and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Create a star rect at (0, 0) and then set correct position.
        # Draw a small white circle.
        self.radius = random.randint(1, 2)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()

        # Start each new star at a random position on the screen.
        self.rect.x = random.randint(0, self.settings.screen_width)
        self.rect.y = random.randint(0, self.settings.screen_height)

        # Store the star's exact vertical position.
        self.y = float(self.rect.y)
        
        # Random speed for depth effect.
        self.speed = random.uniform(0.5, 1.5)

    def update(self):
        """Move the star down the screen."""
        self.y += self.speed
        # If star is at the bottom of the screen, move it to the top.
        if self.y >= self.settings.screen_height:
            self.y = 0
            self.rect.x = random.randint(0, self.settings.screen_width)
        
        self.rect.y = self.y