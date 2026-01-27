import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """A class to manage explosions when an alien is hit."""
    def __init__(self, ai_game, center):
        super().__init__()
        self.screen = ai_game.screen
        self.image = pygame.image.load('images/explosion.png')
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        # Timing for total duration (3 seconds)
        self.start_time = pygame.time.get_ticks()
        # Timing for blinking (0.1 seconds / 100ms)
        self.last_blink = self.start_time
        self.visible = True

    def update(self):
        """Manage the explosion lifetime and blinking."""
        now = pygame.time.get_ticks()
        
        # Check if 3 seconds have passed
        if now - self.start_time >= 3000:
            self.kill()
        
        # Toggle visibility every 100ms
        if now - self.last_blink >= 100:
            self.visible = not self.visible
            self.last_blink = now

    def draw_explosion(self):
        """Draw the explosion if it is currently in a visible blink state."""
        if self.visible:
            self.screen.blit(self.image, self.rect)