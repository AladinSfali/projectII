class Settings:
    """ A class to store all settings for Alien Invasion. """

    def __init__(self):
        """Initialize the game's setting."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        
        # Ship settings
        self.ship_speed = 5.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 10.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents rigth; -1 represents left.
        self.fleet_direction = 1
        self.alien_bullet_speed = 3.0

        # Scoring
        self.alien_points = 50
