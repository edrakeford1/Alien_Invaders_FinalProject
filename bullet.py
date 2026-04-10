"""
Program: bullet.py
Name: Elijah Drakeford
Purpose: a class to manage the bullets fired from the ship
Date: April 10, 2026
Starter Code: Cloned from https://github.com/edrakeford1/Alien_Invaders_Class
"""

import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game):
        """ Create a bullet object at the ship's current position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set the correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midright = ai_game.ship.rect.midright

        # Store the bullet's position as a float
        self.x = float(self.rect.x)

    def update(self):
        """ Move the bullet across the screen """
        # Update the exact position of the bullet
        self.x += self.settings.bullet_speed
        # Update the rect position
        self.rect.x = self.x

    def draw_bullet(self):
        """ Draw the bullet to the screen """
        pygame.draw.rect(self.screen, self.color, self.rect)
