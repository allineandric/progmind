"""This module implements the box object (sprite) for Progmind"""
import pygame
from pygame.sprite import Sprite

class Box(Sprite):
    """Box object"""

    def __init__(self, settings, screen, image):
        """Initialize the box, not much to do other than save the params"""
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.dying = False

    # 'draw' is required by pygame.Sprite.Group for drawing in batches
    def draw(self):
        """Draws the box at its current position on the screen"""
        self.screen.blit(self.image, self.rect)
        