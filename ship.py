import pygame

class Ship:
    """A class to manage the ship."""
    
    def __init__(self, ai_game):
        """Initialize the ship and set the position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        # Pre-render rotations
        self.rotated_surfaces = {}
        for angle in range(0, 360, 45):
            self.rotated_surfaces[angle] = pygame.transform.rotate(self.image, angle)

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement falg; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.angle = 0
        self.visible = True
        
        # Invulnerability settings
        self.invulnerable = False
        self.invulnerable_start_time = 0

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Update the angle based on current movement flags.
        self._update_angle()

        # Update rect object from self.x and self.y.
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Check invulnerability expiration
        if self.invulnerable and pygame.time.get_ticks() - self.invulnerable_start_time > 1000:
            self.invulnerable = False
            self.visible = True

    def _update_angle(self):
        """Determine the angle of the ship based on movement flags."""
        if self.moving_up and self.moving_right:
            self.angle = 315
        elif self.moving_up and self.moving_left:
            self.angle = 45
        elif self.moving_down and self.moving_right:
            self.angle = 225
        elif self.moving_down and self.moving_left:
            self.angle = 135
        elif self.moving_up:
            self.angle = 0
        elif self.moving_down:
            self.angle = 180
        elif self.moving_left:
            self.angle = 90
        elif self.moving_right:
            self.angle = 270

    def center_ship(self):
        """Center the ship on the screen and make it visible."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.visible = True
        
        # Trigger invulnerability
        self.invulnerable = True
        self.invulnerable_start_time = pygame.time.get_ticks()

    def blitme(self):
        """Draw the ship at its current location."""
        if self.invulnerable and (pygame.time.get_ticks() // 200) % 2 == 0:
            return

        if self.visible:
            current_image = self.rotated_surfaces[self.angle]
            new_rect = current_image.get_rect(center=self.rect.center)
            self.screen.blit(current_image, new_rect)
