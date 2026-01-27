import pygame
import random
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()
        self.settings = ai_game.settings

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.level = ai_game.selected_level

        if self.level == 2:
            self.speed_x = random.choice([-1, 1]) * self.settings.alien_speed
            self.speed_y = random.choice([-1, 1]) * self.settings.alien_speed
        
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the alien based on the current level logic."""
        if self.level == 1:
            # Standard fleet movement
            self.x += self.settings.alien_speed * self.settings.fleet_direction
            self.rect.x = self.x
        elif self.level == 2:
            # Random independent movement
            self.x += self.speed_x
            self.y += self.speed_y
            self.rect.x = self.x
            self.rect.y = self.y

            # Bounce off edges
            screen_rect = self.screen.get_rect()
            if self.rect.right >= screen_rect.right or self.rect.left <= 0:
                self.speed_x *= -1
            if self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0:
                self.speed_y *= -1
