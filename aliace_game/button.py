"""
Button UI component for the Elias game.
This module provides a Button class for creating interactive buttons in pygame.
"""

import pygame
from .constants import BLACK, FONT_SIZE_MEDIUM

class Button:
    """A clickable button UI component."""
    
    def __init__(self, x, y, width, height, text, color, hover_color):
        """
        Initialize a new Button.
        
        Args:
            x (int): The x-coordinate of the button's top-left corner
            y (int): The y-coordinate of the button's top-left corner
            width (int): The width of the button
            height (int): The height of the button
            text (str): The text to display on the button
            color (tuple): The RGB color of the button
            hover_color (tuple): The RGB color when the button is hovered over
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        
    def draw(self, screen):
        """
        Draw the button on the screen.
        
        Args:
            screen (pygame.Surface): The screen surface to draw on
        """
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        """
        Check if the mouse is hovering over the button and update its appearance.
        
        Args:
            pos (tuple): The current mouse position (x, y)
            
        Returns:
            bool: True if the mouse is hovering over the button, False otherwise
        """
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        else:
            self.current_color = self.color
            return False
            
    def check_click(self, pos):
        """
        Check if the button was clicked.
        
        Args:
            pos (tuple): The mouse position when clicked (x, y)
            
        Returns:
            bool: True if the button was clicked, False otherwise
        """
        return self.rect.collidepoint(pos)