"""
Word list display component for the Elias game.
This module provides a scrollable word list display for the word management interface.
"""

import pygame
from .constants import BLACK, WHITE, LIGHT_GRAY, FONT_SIZE_SMALL

class WordList:
    """A scrollable word list display component."""
    
    def __init__(self, x, y, width, height, words=None):
        """
        Initialize a new WordList.
        
        Args:
            x (int): The x-coordinate of the list's top-left corner
            y (int): The y-coordinate of the list's top-left corner
            width (int): The width of the list
            height (int): The height of the list
            words (list): Initial list of words to display
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.words = words if words is not None else []
        self.font = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.scroll_offset = 0
        self.item_height = 30
        self.visible_items = height // self.item_height
        
    def update_words(self, words):
        """
        Update the list of words.
        
        Args:
            words (list): New list of words to display
        """
        self.words = words
        
    def handle_event(self, event):
        """
        Handle pygame events for the word list.
        
        Args:
            event: Pygame event
            
        Returns:
            str or None: The clicked word if any, None otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):  # Left click
                # Calculate which word was clicked
                relative_y = event.pos[1] - self.rect.top + self.scroll_offset
                word_index = relative_y // self.item_height
                
                if 0 <= word_index < len(self.words):
                    return self.words[word_index]
            elif event.button == 4 and self.rect.collidepoint(pygame.mouse.get_pos()):  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - self.item_height)
            elif event.button == 5 and self.rect.collidepoint(pygame.mouse.get_pos()):  # Scroll down
                max_scroll = max(0, len(self.words) * self.item_height - self.rect.height)
                self.scroll_offset = min(max_scroll, self.scroll_offset + self.item_height)
                
        return None
        
    def draw(self, screen):
        """
        Draw the word list on the screen.
        
        Args:
            screen (pygame.Surface): The screen surface to draw on
        """
        # Draw background
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Create a clipping area for the list
        clip_rect = self.rect.copy()
        screen.set_clip(clip_rect)
        
        # Draw words
        for i, word in enumerate(self.words):
            word_y = self.rect.top + i * self.item_height - self.scroll_offset
            
            # Only draw words that are visible
            if word_y + self.item_height > self.rect.top and word_y < self.rect.bottom:
                # Highlight on hover
                mouse_pos = pygame.mouse.get_pos()
                word_rect = pygame.Rect(self.rect.left, word_y, self.rect.width, self.item_height)
                
                if word_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, LIGHT_GRAY, word_rect)
                
                # Draw word text
                text_surf = self.font.render(word, True, BLACK)
                text_rect = text_surf.get_rect(midleft=(self.rect.left + 10, word_y + self.item_height // 2))
                screen.blit(text_surf, text_rect)
        
        screen.set_clip(None)