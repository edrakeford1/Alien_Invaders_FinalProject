"""
Program: alien_invasion.py
Name: Elijah Drakeford
Purpose: Changing game mechanics of the Alien Invasion game
Date: April 10, 2026
Starter Code: Cloned from https://github.com/edrakeford1/Alien_Invaders_Class
"""

import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """ Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Set the background color
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # Respond to key presses and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """ Respond to key presses """
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """ Respond to key releases """
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Update position of the bullets and get rid of the old bullet """
        # Update bullet positions
        self.bullets.update()
        
        """ Create a new bullet and add it to the bullets group """
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.screen.width:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Respond to bullet-alien collision """
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """ Check if the fleet is at an edge, then update positions """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting left of the screen
        self._check_aliens_left()
    
    def _update_screen(self):
        """ Update images on the screen, and flip to the new screen """
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def _create_fleet(self):
        """ Create a fleet of aliens """
        # Create an alien and keep adding aliens until there's no room left
        # Spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, alien_height

        while current_x < (self.settings.screen_height - 2 * alien_height):
            while current_y < (self.settings.screen_width - 3 * alien_width):
                self._create_alien(current_x, current_y)
                current_y -= 2 * alien_width

            # Finished a row; reset y value and increment x value
            current_x -= 2 * alien_height
            current_y = alien_width

    def _create_alien(self, x_position, y_position):
        """ Create an alien and place it in the fleet """
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """ Respond appropriately if any aliens have reached an edge """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
            """ Drop the entire fleet and change the fleet's direction  """
            for alien in self.aliens.sprites():
                alien.rect.x += self.settings.fleet_drop_speed
            self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """ Respond to the ship being hit by an alien """
        # Get rid of any remaining bullets and aliens
        self.bullets.empty()
        self.aliens.empty

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        # Pause
        sleep(0.5)

    def _check_aliens_left(self):
        """ Check if any aliens have reached the left of the screen """
        for alien in self.aliens.sprites():
            if alien.rect.left >= self.settings.screen_width:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
