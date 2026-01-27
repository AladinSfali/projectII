import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from explosion import Explosion

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullet = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        # Font for the game over message.
        self.font = pygame.font.SysFont(None, 48)

        # Start Alien Invasion in an inactive state to show the menu.
        self.game_active = False
        self.first_game = True
        self.selected_level = 1

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_explosions()
            self._update_screen()
            self.clock.tick(60)
      
        print(len(self.bullets))
            

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT and self.game_active:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT and self.game_active:
            # Move the ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_UP and self.game_active:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN and self.game_active:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE and self.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_s and self.first_game:
            if self.selected_level in (1, 2):
                self.aliens.empty()
                self._create_fleet()
                self.game_active = True
                self.first_game = False
        elif event.key == pygame.K_r and not self.game_active and not self.first_game:
            self._reset_game()
        elif self.first_game:
            if event.key == pygame.K_UP:
                self.selected_level = max(1, self.selected_level - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_level = min(3, self.selected_level + 1)

    def _check_keyup_events(self, event):   
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
            
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullet) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullet.add(new_bullet)
    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)

        if self.first_game:
            self._draw_menu()
        else:
            for bullet in self.bullet.sprites():
                bullet.draw_bullet()
            self.ship.blitme()
            self.aliens.draw(self.screen)
            for explosion in self.explosions.sprites():
                explosion.draw_explosion()
                
            if not self.game_active:
                self._draw_game_over_message()

        pygame.display.flip()

    def _draw_menu(self):
        """Draw the start menu."""
        # Render Title
        title_font = pygame.font.SysFont(None, 80)
        title_image = title_font.render("ALIEN INVASION", True, (0, 0, 0), self.settings.bg_color)
        title_rect = title_image.get_rect(centerx=self.screen.get_rect().centerx, y=100)
        self.screen.blit(title_image, title_rect)

        # Draw Level Selection Box
        box_width, box_height = 400, 300
        box_rect = pygame.Rect(0, 0, box_width, box_height)
        box_rect.center = self.screen.get_rect().center
        pygame.draw.rect(self.screen, (0, 0, 0), box_rect, 2)

        level_label = self.font.render("SELECT LEVEL", True, (0, 0, 0), self.settings.bg_color)
        level_label_rect = level_label.get_rect(centerx=box_rect.centerx, top=box_rect.top + 10)
        self.screen.blit(level_label, level_label_rect)

        # Level 1
        l1_color = (0, 150, 0) if self.selected_level == 1 else (100, 100, 100)
        l1_text = "> Level 1 <" if self.selected_level == 1 else "  Level 1  "
        l1_image = self.font.render(l1_text, True, l1_color, self.settings.bg_color)
        l1_rect = l1_image.get_rect(centerx=box_rect.centerx, top=level_label_rect.bottom + 40)
        self.screen.blit(l1_image, l1_rect)

        # Level 2
        l2_color = (0, 150, 0) if self.selected_level == 2 else (100, 100, 100)
        l2_text = "> Level 2 <" if self.selected_level == 2 else "  Level 2  "
        l2_image = self.font.render(l2_text, True, l2_color, self.settings.bg_color)
        l2_rect = l2_image.get_rect(centerx=box_rect.centerx, top=l1_rect.bottom + 20)
        self.screen.blit(l2_image, l2_rect)

        # Level 3 (Placeholder)
        l3_color = (0, 150, 0) if self.selected_level == 3 else (100, 100, 100)
        l3_text = "> Level 3 (Locked) <" if self.selected_level == 3 else "  Level 3 (Locked)  "
        l3_image = self.font.render(l3_text, True, l3_color, self.settings.bg_color)
        l3_rect = l3_image.get_rect(centerx=box_rect.centerx, top=l2_rect.bottom + 20)
        self.screen.blit(l3_image, l3_rect)

        # Render instructions
        instructions = f"Press 'S' to Start Level {self.selected_level}"
        if self.selected_level > 2:
            instructions = "Level Locked! Select Level 1 or 2"
        instr_image = self.font.render(instructions, True, (60, 60, 60), self.settings.bg_color)
        instr_rect = instr_image.get_rect(centerx=self.screen.get_rect().centerx, bottom=self.screen.get_rect().bottom - 100)
        self.screen.blit(instr_image, instr_rect)

    def _draw_game_over_message(self):
        """Draw a 'pop-up' style message when the game is over."""
        msg = "GAME OVER! Press 'R' to Restart or 'Q' to Quit"
        msg_image = self.font.render(msg, True, (200, 0, 0), (255, 255, 255))
        msg_rect = msg_image.get_rect()
        msg_rect.center = self.screen.get_rect().center
        
        # Draw a background box for the text
        padding = 20
        bg_rect = pygame.Rect(0, 0, msg_rect.width + padding, msg_rect.height + padding)
        bg_rect.center = msg_rect.center
        
        pygame.draw.rect(self.screen, (255, 255, 255), bg_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect, 2)
        self.screen.blit(msg_image, msg_rect)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullet position
        self.bullet.update()

        # Get rid of bullets that have disappeared off any edge.
        for bullet in self.bullet.copy():
            if (bullet.rect.bottom <= 0 or 
                bullet.rect.top >= self.settings.screen_height or
                bullet.rect.right <= 0 or 
                bullet.rect.left >= self.settings.screen_width):
                self.bullet.remove(bullet)

        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullet, self.aliens, True, True)
        if collisions:
            for aliens_hit in collisions.values():
                for alien in aliens_hit:
                    new_explosion = Explosion(self, alien.rect.center)
                    self.explosions.add(new_explosion)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        if self.selected_level == 1:
            self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Create explosion at ship's position.
        new_explosion = Explosion(self, self.ship.rect.center)
        self.explosions.add(new_explosion)
        
        self.ship.visible = False
        self.game_active = False
        
    def _reset_game(self):
        """Reset the game to start a new round."""
        # Clear out any remaining aliens, bullets, and explosions.
        self.aliens.empty()
        self.bullet.empty()
        self.explosions.empty()
        
        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()
        
        # Restart the game state.
        self.game_active = True

    def _update_explosions(self):
        """Update the positions/state of all explosions."""
        self.explosions.update()
        
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 4 * alien_width

            # Finished a row; rest x value, and increment y value.
            current_x = alien_width
            current_y += 8 * alien_height


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.y = y_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
