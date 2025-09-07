"""
Main game logic for the Elias game.
This module contains the main game class and all game mechanics.
"""

import pygame
import threading
import time
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, GREEN, RED, BLUE, 
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL, GAME_DURATION
)
from .words import Words
from .button import Button

class EliasGame:
    """Main game class that handles game logic, UI, and events."""
    
    def __init__(self):
        """Initialize the game."""
        # Initialize pygame
        pygame.init()
        
        # Initialize pygame display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Игра 'Элиас'")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.word_manager = Words()
        self.score = 0
        self.current_word = None
        self.game_active = False
        self.game_finished = False
        self.time_left = GAME_DURATION
        self.start_time = 0
        self.end_time = 0
        
        # Fonts
        self.large_font = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.medium_font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.small_font = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        # Buttons
        self.guessed_button = Button(
            WINDOW_WIDTH // 4 - 100, 
            WINDOW_HEIGHT - 100, 
            200, 50, 
            "Угадано", 
            GREEN, 
            (0, 255, 0)
        )
        
        self.skip_button = Button(
            3 * WINDOW_WIDTH // 4 - 100, 
            WINDOW_HEIGHT - 100, 
            200, 50, 
            "Пропустить", 
            RED, 
            (255, 0, 0)
        )
        
        self.replay_button = Button(
            WINDOW_WIDTH // 2 - 100, 
            WINDOW_HEIGHT - 100, 
            200, 50, 
            "Играть снова", 
            BLUE, 
            (100, 150, 255)
        )
        
        # Timer thread
        self.timer_thread = None
        self.timer_running = False
        
    def start_timer(self):
        """Start the timer in a separate thread."""
        self.timer_running = True
        self.timer_thread = threading.Thread(target=self.timer_function)
        self.timer_thread.daemon = True
        self.timer_thread.start()
        
    def timer_function(self):
        """Timer function that runs in a separate thread."""
        while self.timer_running and self.game_active:
            current_time = time.time()
            if current_time < self.end_time:
                self.time_left = int(self.end_time - current_time)
            else:
                self.time_left = 0
                self.game_active = False
                self.game_finished = True
            time.sleep(0.1)  # Update 10 times per second for smooth display
            
    def start_game(self):
        """Starts the game."""
        self.score = 0
        self.game_active = True
        self.game_finished = False
        self.time_left = GAME_DURATION
        self.start_time = time.time()
        self.end_time = self.start_time + GAME_DURATION
        
        # Get first word
        self.current_word = self.word_manager.get_random_word()
        if self.current_word is None:
            self.current_word = "Нет слов"
            
        # Start timer
        self.start_timer()
        
    def next_word(self):
        """Get the next word."""
        self.current_word = self.word_manager.get_random_word()
        if self.current_word is None:
            self.current_word = "Все слова использованы!"
            self.game_active = False
            self.game_finished = True
            
    def handle_events(self):
        """
        Handle pygame events.
        
        Returns:
            bool: True if the game should continue running, False to exit
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if self.game_active:
                    self.guessed_button.check_hover(mouse_pos)
                    self.skip_button.check_hover(mouse_pos)
                elif self.game_finished:
                    self.replay_button.check_hover(mouse_pos)
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if self.game_active:
                        if self.guessed_button.check_click(mouse_pos):
                            self.score += 1
                            self.next_word()
                        elif self.skip_button.check_click(mouse_pos):
                            self.next_word()
                    elif self.game_finished:
                        if self.replay_button.check_click(mouse_pos):
                            self.start_game()
                            
        return True
        
    def draw_game_screen(self):
        """Draw the main game screen."""
        self.screen.fill(WHITE)
        
        # Draw score
        score_text = self.medium_font.render(f"Счёт: {self.score}", True, BLACK)
        self.screen.blit(score_text, (20, 20))
        
        # Draw timer
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        timer_text = self.medium_font.render(f"Время: {minutes:02d}:{seconds:02d}", True, BLACK)
        self.screen.blit(timer_text, (WINDOW_WIDTH - timer_text.get_width() - 20, 20))
        
        # Draw current word
        if self.current_word:
            word_text = self.large_font.render(self.current_word.upper(), True, BLACK)
            word_rect = word_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            self.screen.blit(word_text, word_rect)
            
            # Draw instruction
            instruction_text = self.small_font.render("Объясните это слово команде", True, (128, 128, 128))
            instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
            self.screen.blit(instruction_text, instruction_rect)
        
        # Draw buttons
        self.guessed_button.draw(self.screen)
        self.skip_button.draw(self.screen)
        
        pygame.display.flip()
        
    def draw_results_screen(self):
        """Draw the results screen."""
        self.screen.fill(WHITE)
        
        # Draw title
        title_text = self.large_font.render("ИГРА ОКОНЧЕНА!", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw score
        score_text = self.medium_font.render(f"Ваш итоговый счёт: {self.score}", True, BLACK)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, 200))
        self.screen.blit(score_text, score_rect)
        
        # Draw performance evaluation
        if self.score >= 15:
            evaluation_text = self.medium_font.render("Отличный результат! Вы мастер объяснений! 🏆", True, GREEN)
        elif self.score >= 10:
            evaluation_text = self.medium_font.render("Хороший результат! 👍", True, BLUE)
        elif self.score >= 5:
            evaluation_text = self.medium_font.render("Неплохо! Можно лучше 😊", True, BLACK)
        else:
            evaluation_text = self.medium_font.render("Практика делает мастера! Попробуйте ещё раз! 💪", True, RED)
            
        evaluation_rect = evaluation_text.get_rect(center=(WINDOW_WIDTH//2, 300))
        self.screen.blit(evaluation_text, evaluation_rect)
        
        # Draw replay button
        self.replay_button.draw(self.screen)
        
        pygame.display.flip()
        
    def run(self):
        """
        Main game loop.
        This method starts the game and runs the main loop until the user exits.
        """
        self.start_game()
        
        running = True
        while running:
            running = self.handle_events()
            
            if self.game_active:
                self.draw_game_screen()
            elif self.game_finished:
                self.draw_results_screen()
                
            self.clock.tick(60)  # 60 FPS
            
        # Clean up
        self.timer_running = False
        pygame.quit()