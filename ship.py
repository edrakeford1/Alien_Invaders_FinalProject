import pygame

class Ship:
    """ A class to manage the ship """

    def __init__(self, ai_game):
        """ Initialize the ship and set its starting position """
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.imagerotated = pygame.transform.rotate(self.image, 270)
        self.rect = self.imagerotated.get_rect()

        # Start each new ship at the middle of the screen on the left side
        self.rect.midleft = self.screen_rect.midleft

        # Store a float for the ship's exact vertical position
        self.y = float(self.rect.y)

        # Movement flag; starts with a ship that is not moving
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """ Update the ship's position based on the movement flag """
        # Update the ship's y value, not the rect
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Update rect object from self.y
        self.rect.y = self.y

    def blitme(self):
        """ Draw the ship at its current location """

        self.screen.blit(self.imagerotated, self.rect)
