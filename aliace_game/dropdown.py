"""
Dropdown component for the Elias game.
This module provides a Dropdown class for creating dropdown menus in pygame.
"""

import pygame
from .constants import BLACK, WHITE, LIGHT_GRAY, GRAY, FONT_SIZE_SMALL

class Dropdown:
    """A dropdown menu UI component."""
    
    def __init__(self, x, y, width, height, options, selected=0):
        """
        Initialize a new Dropdown.
        
        Args:
            x (int): The x-coordinate of the dropdown's top-left corner
            y (int): The y-coordinate of the dropdown's top-left corner
            width (int): The width of the dropdown
            height (int): The height of the dropdown
            options (list): List of options to display
            selected (int): Index of the initially selected option
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected = selected
        self.font = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.expanded = False
        self.option_height = 30
        self.max_visible_options = 5
        
    def handle_event(self, event):
        """
        Handle pygame events for the dropdown.
        
        Args:
            event: Pygame event
            
        Returns:
            bool: True if the selection changed, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check if clicking on the dropdown
                if self.rect.collidepoint(event.pos):
                    self.expanded = not self.expanded
                    return False
                    
                # Check if clicking on an option when expanded
                if self.expanded:
                    # Calculate options area
                    options_height = min(len(self.options), self.max_visible_options) * self.option_height
                    options_rect = pygame.Rect(
                        self.rect.left, 
                        self.rect.bottom, 
                        self.rect.width, 
                        options_height
                    )
                    
                    if options_rect.collidepoint(event.pos):
                        # Calculate which option was clicked
                        option_index = (event.pos[1] - self.rect.bottom) // self.option_height
                        if 0 <= option_index < len(self.options):
                            self.selected = option_index
                            self.expanded = False
                            return True
                    else:
                        # Clicked outside, close dropdown
                        self.expanded = False
                        
        elif event.type == pygame.MOUSEBUTTONUP:
            # Close dropdown if mouse is released outside
            if self.expanded and not self.rect.collidepoint(pygame.mouse.get_pos()):
                # Check if release is outside the options area too
                options_height = min(len(self.options), self.max_visible_options) * self.option_height
                options_rect = pygame.Rect(
                    self.rect.left, 
                    self.rect.bottom, 
                    self.rect.width, 
                    options_height
                )
                if not options_rect.collidepoint(pygame.mouse.get_pos()):
                    self.expanded = False
                    
        return False
        
    def get_selected_option(self):
        """
        Get the currently selected option.
        
        Returns:
            str: The selected option
        """
        return self.options[self.selected] if 0 <= self.selected < len(self.options) else ""
        
    def set_selected_option(self, option):
        """
        Set the selected option.
        
        Args:
            option (str): The option to select
        """
        try:
            self.selected = self.options.index(option)
        except ValueError:
            pass  # Option not found, keep current selection
            
    def draw(self, screen):
        """
        Draw the dropdown on the screen.
        
        Args:
            screen (pygame.Surface): The screen surface to draw on
        """
        # Draw main dropdown
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw selected option
        selected_text = self.font.render(self.get_selected_option(), True, BLACK)
        screen.blit(selected_text, (self.rect.left + 5, self.rect.centery - selected_text.get_height() // 2))
        
        # Draw arrow
        arrow_points = [
            (self.rect.right - 20, self.rect.centery - 5),
            (self.rect.right - 10, self.rect.centery - 5),
            (self.rect.right - 15, self.rect.centery + 5)
        ]
        pygame.draw.polygon(screen, BLACK, arrow_points)
        
        # Draw options if expanded
        if self.expanded:
            # Calculate visible options
            visible_options = self.options[:self.max_visible_options]
            options_height = len(visible_options) * self.option_height
            
            # Draw background
            options_rect = pygame.Rect(
                self.rect.left, 
                self.rect.bottom, 
                self.rect.width, 
                options_height
            )
            pygame.draw.rect(screen, WHITE, options_rect)
            pygame.draw.rect(screen, BLACK, options_rect, 2)
            
            # Draw options
            for i, option in enumerate(visible_options):
                option_rect = pygame.Rect(
                    self.rect.left, 
                    self.rect.bottom + i * self.option_height, 
                    self.rect.width, 
                    self.option_height
                )
                
                # Highlight on hover
                if option_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, LIGHT_GRAY, option_rect)
                    
                # Highlight selected option
                if i == self.selected:
                    pygame.draw.rect(screen, (173, 216, 230), option_rect)
                
                option_text = self.font.render(option, True, BLACK)
                screen.blit(option_text, (self.rect.left + 5, option_rect.centery - option_text.get_height() // 2))