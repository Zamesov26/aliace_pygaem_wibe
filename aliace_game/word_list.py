"""
Word list display component for the Elias game.
This module provides a scrollable word list display for the word management interface.
"""

import pygame
from .constants import BLACK, WHITE, LIGHT_GRAY, GRAY, FONT_SIZE_SMALL

class WordList:
    """A scrollable word list display component with selection functionality."""
    
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
        # Words should be tuples of (word, difficulty)
        self.words = words if words is not None else []
        self.font = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.scroll_offset = 0
        self.item_height = 30
        self.visible_items = height // self.item_height
        self.selected_word = None
        self.selected_index = -1
        
        # Scrollbar properties
        self.scrollbar_width = 15
        self.scrollbar_rect = pygame.Rect(
            self.rect.right - self.scrollbar_width, 
            self.rect.top, 
            self.scrollbar_width, 
            self.rect.height
        )
        self.scrollbar_dragging = False
        self.scrollbar_drag_offset = 0
        
    def update_words(self, words):
        """
        Update the list of words.
        
        Args:
            words (list): New list of words to display (tuples of (word, difficulty))
        """
        self.words = words
        # Reset selection when updating words
        self.selected_word = None
        self.selected_index = -1
        # Reset scroll offset when updating words
        self.scroll_offset = 0
        
    def handle_event(self, event):
        """
        Handle pygame events for the word list.
        
        Args:
            event: Pygame event
            
        Returns:
            str or None: Action to perform or None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check if clicking on scrollbar
                if self.scrollbar_rect.collidepoint(event.pos):
                    self.scrollbar_dragging = True
                    # Calculate drag offset
                    if len(self.words) > 0:
                        max_scroll = max(1, len(self.words) * self.item_height - self.rect.height)
                        if max_scroll > 0:
                            scrollbar_height = max(20, (self.rect.height * self.rect.height) / (len(self.words) * self.item_height))
                            scrollbar_y = self.rect.top + (self.scroll_offset * (self.rect.height - scrollbar_height)) / max_scroll
                            self.scrollbar_drag_offset = event.pos[1] - scrollbar_y
                    
                # Check if clicking on word
                elif self.rect.collidepoint(event.pos) and not self.scrollbar_rect.collidepoint(event.pos):
                    # Calculate which word was clicked
                    relative_y = event.pos[1] - self.rect.top + self.scroll_offset
                    word_index = relative_y // self.item_height
                    
                    if 0 <= word_index < len(self.words):
                        self.selected_word = self.words[word_index][0]  # Store just the word
                        self.selected_index = word_index
                        return "select"  # Indicate a word was selected
                        
            elif event.button == 4 and self.rect.collidepoint(pygame.mouse.get_pos()):  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - self.item_height)
            elif event.button == 5 and self.rect.collidepoint(pygame.mouse.get_pos()):  # Scroll down
                max_scroll = max(0, len(self.words) * self.item_height - self.rect.height)
                self.scroll_offset = min(max_scroll, self.scroll_offset + self.item_height)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button released
                self.scrollbar_dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.scrollbar_dragging:
                # Calculate new scroll position based on mouse position
                mouse_y = event.pos[1] - self.scrollbar_drag_offset
                # Clamp to valid range
                max_scroll = max(0, len(self.words) * self.item_height - self.rect.height)
                if max_scroll > 0:
                    # Convert mouse position to scroll offset
                    scroll_ratio = max(0, min(1, (mouse_y - self.rect.top) / self.rect.height))
                    self.scroll_offset = int(scroll_ratio * max_scroll)
                else:
                    self.scroll_offset = 0
                
        return None
        
    def get_selected_word_info(self):
        """
        Get the selected word and its difficulty.
        
        Returns:
            tuple: (word, difficulty) or None if no word selected
        """
        if self.selected_word is not None and 0 <= self.selected_index < len(self.words):
            return self.words[self.selected_index]
        return None
        
    def clear_selection(self):
        """Clear the current selection."""
        self.selected_word = None
        self.selected_index = -1
        
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
        clip_rect.width -= self.scrollbar_width  # Leave space for scrollbar
        screen.set_clip(clip_rect)
        
        # Draw words
        for i, (word, difficulty) in enumerate(self.words):
            word_y = self.rect.top + i * self.item_height - self.scroll_offset
            
            # Only draw words that are visible
            if word_y + self.item_height > self.rect.top and word_y < self.rect.bottom:
                # Highlight selected word
                word_rect = pygame.Rect(self.rect.left, word_y, self.rect.width - self.scrollbar_width, self.item_height)
                
                if i == self.selected_index:
                    pygame.draw.rect(screen, (173, 216, 230), word_rect)  # Light blue for selection
                elif word_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, LIGHT_GRAY, word_rect)
                
                # Draw word text
                text_surf = self.font.render(f"{word} ({difficulty})", True, BLACK)
                text_rect = text_surf.get_rect(midleft=(self.rect.left + 10, word_y + self.item_height // 2))
                screen.blit(text_surf, text_rect)
        
        screen.set_clip(None)
        
        # Draw scrollbar
        if len(self.words) > 0:
            max_scroll = max(0, len(self.words) * self.item_height - self.rect.height)
            if max_scroll > 0:
                # Calculate scrollbar dimensions
                scrollbar_height = max(20, (self.rect.height * self.rect.height) / (len(self.words) * self.item_height))
                scrollbar_height = min(scrollbar_height, self.rect.height)
                
                # Calculate scrollbar position
                scrollbar_y = self.rect.top + (self.scroll_offset * (self.rect.height - scrollbar_height)) / max_scroll
                
                # Update scrollbar rect
                self.scrollbar_rect = pygame.Rect(
                    self.rect.right - self.scrollbar_width,
                    scrollbar_y,
                    self.scrollbar_width,
                    scrollbar_height
                )
                
                # Draw scrollbar
                pygame.draw.rect(screen, GRAY, self.scrollbar_rect)
                pygame.draw.rect(screen, BLACK, self.scrollbar_rect, 1)
            else:
                # No scrolling needed, draw a minimal scrollbar
                self.scrollbar_rect = pygame.Rect(
                    self.rect.right - self.scrollbar_width,
                    self.rect.top,
                    self.scrollbar_width,
                    self.rect.height
                )
                pygame.draw.rect(screen, GRAY, self.scrollbar_rect)
                pygame.draw.rect(screen, BLACK, self.scrollbar_rect, 1)