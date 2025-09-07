"""
Text input component for the Elias game.
This module provides a TextInput class for creating text input fields in pygame.
"""

import pygame
from .constants import BLACK, WHITE, GRAY, FONT_SIZE_SMALL

class TextInput:
    """A text input UI component."""
    
    def __init__(self, x, y, width, height, placeholder="", initial_text=""):
        """
        Initialize a new TextInput.
        
        Args:
            x (int): The x-coordinate of the input's top-left corner
            y (int): The y-coordinate of the input's top-left corner
            width (int): The width of the input
            height (int): The height of the input
            placeholder (str): Placeholder text to show when input is empty
            initial_text (str): Initial text in the input field
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.placeholder = placeholder
        self.text = initial_text
        self.active = False
        self.font = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def handle_event(self, event):
        """
        Handle pygame events for the text input.
        
        Args:
            event: Pygame event
            
        Returns:
            bool: True if the event was handled, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state based on mouse click
            self.active = self.rect.collidepoint(event.pos)
            return True
            
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.active = False
            else:
                # Add character to text (only allow Cyrillic, Latin and spaces)
                char = event.unicode
                if char.isalpha() or char.isspace() or any(ord(c) > 1000 for c in char):
                    self.text += char
            return True
            
        return False
        
    def update(self, dt):
        """
        Update the text input state.
        
        Args:
            dt (float): Time delta since last update
        """
        if self.active:
            self.cursor_timer += dt
            # Blink cursor every 0.5 seconds
            if self.cursor_timer >= 500:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
        else:
            self.cursor_visible = False
            self.cursor_timer = 0
        
    def draw(self, screen):
        """
        Draw the text input on the screen.
        
        Args:
            screen (pygame.Surface): The screen surface to draw on
        """
        # Draw input box
        color = BLACK if self.active else GRAY
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)
        
        # Draw text
        display_text = self.text if self.text else self.placeholder
        text_color = BLACK if self.text else GRAY
        text_surf = self.font.render(display_text, True, text_color)
        
        # Position text with some padding
        text_rect = text_surf.get_rect(midleft=(self.rect.left + 5, self.rect.centery))
        
        # If text is too wide, only show the end
        if text_rect.width > self.rect.width - 10:
            # Create a subsurface to clip the text
            clip_rect = pygame.Rect(self.rect.left + 5, self.rect.top, self.rect.width - 10, self.rect.height)
            screen.set_clip(clip_rect)
            screen.blit(text_surf, text_rect)
            screen.set_clip(None)
        else:
            screen.blit(text_surf, text_rect)
        
        # Draw cursor if active
        if self.active and self.cursor_visible:
            cursor_x = text_rect.left + text_surf.get_width()
            if not self.text:  # If no text, start at the beginning
                cursor_x = self.rect.left + 5
            pygame.draw.line(screen, BLACK, (cursor_x, self.rect.top + 5), 
                           (cursor_x, self.rect.bottom - 5), 2)
        
    def get_text(self):
        """
        Get the current text in the input field.
        
        Returns:
            str: Current text
        """
        return self.text
        
    def set_text(self, text):
        """
        Set the text in the input field.
        
        Args:
            text (str): Text to set
        """
        self.text = text
        
    def clear(self):
        """Clear the text in the input field."""
        self.text = ""
        
    def is_active(self):
        """
        Check if the input field is active.
        
        Returns:
            bool: True if active, False otherwise
        """
        return self.active