"""
Main game logic for the Elias game.
This module contains the main game class and all game mechanics.
"""

import pygame
import threading
import time
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, GREEN, RED, BLUE, LIGHT_GRAY,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL, 
    GAME_DURATION_EASY, GAME_DURATION_MEDIUM, GAME_DURATION_HARD,
    SCREEN_MENU, SCREEN_GAME, SCREEN_RESULTS, SCREEN_MANAGE
)
from .words import Words
from .button import Button
from .text_input import TextInput
from .word_list import WordList

class EliasGame:
    """Main game class that handles game logic, UI, and events."""
    
    def __init__(self, db_path="words.db"):
        """
        Initialize the game.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        # Initialize pygame
        pygame.init()
        
        # Initialize pygame display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Игра 'Элиас'")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.word_manager = Words(db_path)
        self.score = 0
        self.current_word = None
        self.game_active = False
        self.game_finished = False
        self.time_left = GAME_DURATION_MEDIUM
        self.start_time = 0
        self.end_time = 0
        self.current_screen = SCREEN_MENU
        self.selected_difficulty = "medium"
        
        # Fonts
        self.large_font = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.medium_font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.small_font = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        # Menu screen buttons
        button_width = 300
        button_height = 60
        start_y = WINDOW_HEIGHT // 2 - 60
        
        self.start_game_button = Button(
            WINDOW_WIDTH // 2 - button_width // 2,
            start_y,
            button_width,
            button_height,
            "Начать игру",
            GREEN,
            (0, 255, 0)
        )
        
        self.manage_words_button = Button(
            WINDOW_WIDTH // 2 - button_width // 2,
            start_y + 80,
            button_width,
            button_height,
            "Управление словами",
            BLUE,
            (100, 150, 255)
        )
        
        self.quit_button = Button(
            WINDOW_WIDTH // 2 - button_width // 2,
            start_y + 160,
            button_width,
            button_height,
            "Выход",
            RED,
            (255, 0, 0)
        )
        
        # Difficulty selection buttons
        self.easy_button = Button(
            WINDOW_WIDTH // 2 - 150,
            WINDOW_HEIGHT // 2 + 20,
            100,
            50,
            "Легко",
            GREEN if self.selected_difficulty == "easy" else LIGHT_GRAY,
            (0, 255, 0) if self.selected_difficulty == "easy" else (220, 220, 220),
            FONT_SIZE_SMALL
        )
        
        self.medium_button = Button(
            WINDOW_WIDTH // 2 - 50,
            WINDOW_HEIGHT // 2 + 20,
            100,
            50,
            "Средне",
            GREEN if self.selected_difficulty == "medium" else LIGHT_GRAY,
            (0, 255, 0) if self.selected_difficulty == "medium" else (220, 220, 220),
            FONT_SIZE_SMALL
        )
        
        self.hard_button = Button(
            WINDOW_WIDTH // 2 + 50,
            WINDOW_HEIGHT // 2 + 20,
            100,
            50,
            "Сложно",
            GREEN if self.selected_difficulty == "hard" else LIGHT_GRAY,
            (0, 255, 0) if self.selected_difficulty == "hard" else (220, 220, 220),
            FONT_SIZE_SMALL
        )
        
        self.confirm_difficulty_button = Button(
            WINDOW_WIDTH // 2 - 100,
            WINDOW_HEIGHT // 2 + 100,
            200,
            50,
            "Подтвердить",
            GREEN,
            (0, 255, 0),
            FONT_SIZE_SMALL
        )
        
        self.back_from_difficulty_button = Button(
            20,
            20,
            100,
            40,
            "Назад",
            LIGHT_GRAY,
            (220, 220, 220),
            FONT_SIZE_SMALL
        )
        
        # Game screen buttons
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
        
        # Management screen buttons
        self.back_button = Button(
            20, 
            20, 
            100, 40, 
            "Назад", 
            LIGHT_GRAY, 
            (220, 220, 220),
            FONT_SIZE_SMALL
        )
        
        self.add_word_button = Button(
            WINDOW_WIDTH - 150, 
            100, 
            130, 40, 
            "Добавить", 
            GREEN, 
            (0, 255, 0),
            FONT_SIZE_SMALL
        )
        
        self.remove_word_button = Button(
            WINDOW_WIDTH - 150, 
            150, 
            130, 40, 
            "Удалить", 
            RED, 
            (255, 0, 0),
            FONT_SIZE_SMALL
        )
        
        # Management screen UI components
        self.word_input = TextInput(
            50, 
            100, 
            WINDOW_WIDTH - 250, 
            40, 
            "Введите новое слово..."
        )
        
        self.word_list = WordList(
            50, 
            170, 
            WINDOW_WIDTH - 250, 
            WINDOW_HEIGHT - 250,
            self.word_manager.get_all_words()
        )
        
        self.message = ""
        self.message_timer = 0
        
        # Timer thread
        self.timer_thread = None
        self.timer_running = False
        
    def get_duration_for_difficulty(self, difficulty):
        """
        Get game duration based on difficulty.
        
        Args:
            difficulty (str): Difficulty level ("easy", "medium", "hard")
            
        Returns:
            int: Duration in seconds
        """
        if difficulty == "easy":
            return GAME_DURATION_EASY
        elif difficulty == "hard":
            return GAME_DURATION_HARD
        else:  # medium
            return GAME_DURATION_MEDIUM
        
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
        self.current_screen = SCREEN_GAME
        self.time_left = self.get_duration_for_difficulty(self.selected_difficulty)
        self.start_time = time.time()
        self.end_time = self.start_time + self.time_left
        
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
            
    def show_manage_screen(self):
        """Show the word management screen."""
        self.current_screen = SCREEN_MANAGE
        # Refresh word list
        self.word_list.update_words(self.word_manager.get_all_words())
        # Clear input and message
        self.word_input.clear()
        self.message = ""
        
    def show_difficulty_selection(self):
        """Show the difficulty selection screen."""
        self.current_screen = "difficulty"
        
    def select_difficulty(self, difficulty):
        """
        Select game difficulty.
        
        Args:
            difficulty (str): Difficulty level ("easy", "medium", "hard")
        """
        self.selected_difficulty = difficulty
        # Update button colors
        self.easy_button.current_color = GREEN if difficulty == "easy" else LIGHT_GRAY
        self.medium_button.current_color = GREEN if difficulty == "medium" else LIGHT_GRAY
        self.hard_button.current_color = GREEN if difficulty == "hard" else LIGHT_GRAY
        
    def add_word(self):
        """Add a new word from the input field."""
        word = self.word_input.get_text().strip().lower()
        if not word:
            self.message = "Введите слово для добавления"
            self.message_timer = 180  # 3 seconds at 60 FPS
            return
            
        if self.word_manager.word_exists(word):
            self.message = f"Слово '{word}' уже существует"
            self.message_timer = 180
            return
            
        if self.word_manager.add_word(word):
            self.message = f"Слово '{word}' добавлено"
            self.word_input.clear()
            # Refresh word list
            self.word_list.update_words(self.word_manager.get_all_words())
        else:
            self.message = "Ошибка при добавлении слова"
        self.message_timer = 180
        
    def remove_word(self, word):
        """Remove a word."""
        if word:
            if self.word_manager.remove_word(word):
                self.message = f"Слово '{word}' удалено"
                # Refresh word list
                self.word_list.update_words(self.word_manager.get_all_words())
            else:
                self.message = f"Ошибка при удалении слова '{word}'"
            self.message_timer = 180
        
    def handle_events(self):
        """
        Handle pygame events.
        
        Returns:
            bool: True if the game should continue running, False to exit
        """
        dt = self.clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if self.current_screen == SCREEN_MENU:
                # Handle menu screen events
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self.start_game_button.check_hover(mouse_pos)
                    self.manage_words_button.check_hover(mouse_pos)
                    self.quit_button.check_hover(mouse_pos)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        if self.start_game_button.check_click(mouse_pos):
                            self.show_difficulty_selection()
                        elif self.manage_words_button.check_click(mouse_pos):
                            self.show_manage_screen()
                        elif self.quit_button.check_click(mouse_pos):
                            return False
                            
            elif self.current_screen == "difficulty":
                # Handle difficulty selection events
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self.easy_button.check_hover(mouse_pos)
                    self.medium_button.check_hover(mouse_pos)
                    self.hard_button.check_hover(mouse_pos)
                    self.confirm_difficulty_button.check_hover(mouse_pos)
                    self.back_from_difficulty_button.check_hover(mouse_pos)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        if self.easy_button.check_click(mouse_pos):
                            self.select_difficulty("easy")
                        elif self.medium_button.check_click(mouse_pos):
                            self.select_difficulty("medium")
                        elif self.hard_button.check_click(mouse_pos):
                            self.select_difficulty("hard")
                        elif self.confirm_difficulty_button.check_click(mouse_pos):
                            self.start_game()
                        elif self.back_from_difficulty_button.check_click(mouse_pos):
                            self.current_screen = SCREEN_MENU
                            
            elif self.current_screen == SCREEN_MANAGE:
                # Handle management screen events
                self.word_input.handle_event(event)
                
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self.back_button.check_hover(mouse_pos)
                    self.add_word_button.check_hover(mouse_pos)
                    self.remove_word_button.check_hover(mouse_pos)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        
                        if self.back_button.check_click(mouse_pos):
                            self.current_screen = SCREEN_MENU
                            
                        elif self.add_word_button.check_click(mouse_pos):
                            self.add_word()
                            
                        elif self.remove_word_button.check_click(mouse_pos):
                            # For simplicity, we'll just show a message
                            # In a more complex implementation, we might allow selecting words
                            self.message = "Кликните на слово в списке для удаления"
                            self.message_timer = 180
                            
                        else:
                            # Check if a word in the list was clicked
                            clicked_word = self.word_list.handle_event(event)
                            if clicked_word:
                                self.remove_word(clicked_word)
                                
            elif self.current_screen == SCREEN_GAME:
                # Handle game screen events
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
                                self.show_difficulty_selection()
                                
            elif self.current_screen == SCREEN_RESULTS:
                # Handle results screen events (same as game screen for replay button)
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self.replay_button.check_hover(mouse_pos)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        if self.replay_button.check_click(mouse_pos):
                            self.show_difficulty_selection()
                            
        # Update text input
        if self.current_screen == SCREEN_MANAGE:
            self.word_input.update(dt)
            
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
            
        return True
        
    def draw_menu_screen(self):
        """Draw the main menu screen."""
        self.screen.fill(WHITE)
        
        # Draw title
        title_text = self.large_font.render("Игра 'Элиас'", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
        self.screen.blit(title_text, title_rect)
        
        # Draw buttons
        self.start_game_button.draw(self.screen)
        self.manage_words_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        
        pygame.display.flip()
        
    def draw_difficulty_screen(self):
        """Draw the difficulty selection screen."""
        self.screen.fill(WHITE)
        
        # Draw title
        title_text = self.large_font.render("Выберите сложность", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
        self.screen.blit(title_text, title_rect)
        
        # Draw difficulty description
        if self.selected_difficulty == "easy":
            desc_text = self.small_font.render("Легко: 3 минуты", True, BLACK)
        elif self.selected_difficulty == "hard":
            desc_text = self.small_font.render("Сложно: 1 минута", True, BLACK)
        else:  # medium
            desc_text = self.small_font.render("Средне: 2 минуты", True, BLACK)
            
        desc_rect = desc_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3 + 30))
        self.screen.blit(desc_text, desc_rect)
        
        # Draw buttons
        self.easy_button.draw(self.screen)
        self.medium_button.draw(self.screen)
        self.hard_button.draw(self.screen)
        self.confirm_difficulty_button.draw(self.screen)
        self.back_from_difficulty_button.draw(self.screen)
        
        pygame.display.flip()
        
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
        
        # Draw difficulty info
        if self.selected_difficulty == "easy":
            diff_text = self.small_font.render("Сложность: Легко", True, BLACK)
        elif self.selected_difficulty == "hard":
            diff_text = self.small_font.render("Сложность: Сложно", True, BLACK)
        else:  # medium
            diff_text = self.small_font.render("Сложность: Средне", True, BLACK)
        diff_rect = diff_text.get_rect(center=(WINDOW_WIDTH//2, 240))
        self.screen.blit(diff_text, diff_rect)
        
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
        
    def draw_manage_screen(self):
        """Draw the word management screen."""
        self.screen.fill(WHITE)
        
        # Draw title
        title_text = self.large_font.render("Управление словами", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 40))
        self.screen.blit(title_text, title_rect)
        
        # Draw word count
        count_text = self.small_font.render(f"Всего слов: {self.word_manager.get_word_count()}", True, BLACK)
        self.screen.blit(count_text, (50, 70))
        
        # Draw input field
        self.word_input.draw(self.screen)
        
        # Draw buttons
        self.back_button.draw(self.screen)
        self.add_word_button.draw(self.screen)
        self.remove_word_button.draw(self.screen)
        
        # Draw word list
        self.word_list.draw(self.screen)
        
        # Draw message if exists
        if self.message and self.message_timer > 0:
            message_color = RED if "Ошибка" in self.message or "уже существует" in self.message else GREEN
            if "Кликните" in self.message:
                message_color = (128, 128, 128)
            message_text = self.small_font.render(self.message, True, message_color)
            self.screen.blit(message_text, (50, WINDOW_HEIGHT - 50))
        
        pygame.display.flip()
        
    def run(self):
        """
        Main game loop.
        This method starts the game and runs the main loop until the user exits.
        """
        running = True
        while running:
            running = self.handle_events()
            
            if self.current_screen == SCREEN_MENU:
                self.draw_menu_screen()
            elif self.current_screen == "difficulty":
                self.draw_difficulty_screen()
            elif self.current_screen == SCREEN_GAME:
                if self.game_active:
                    self.draw_game_screen()
                elif self.game_finished:
                    self.current_screen = SCREEN_RESULTS
                    self.draw_results_screen()
            elif self.current_screen == SCREEN_RESULTS:
                self.draw_results_screen()
            elif self.current_screen == SCREEN_MANAGE:
                self.draw_manage_screen()
                
            self.clock.tick(60)  # 60 FPS
            
        # Clean up
        self.timer_running = False
        pygame.quit()