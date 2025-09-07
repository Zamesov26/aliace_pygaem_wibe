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
    DEFAULT_GAME_DURATION, TIME_OPTIONS,
    SCREEN_MENU, SCREEN_GAME, SCREEN_RESULTS, SCREEN_MANAGE
)
from .words import Words
from .button import Button
from .text_input import TextInput
from .word_list import WordList
from .dropdown import Dropdown

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
        self.time_left = DEFAULT_GAME_DURATION
        self.selected_time = DEFAULT_GAME_DURATION
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
            WINDOW_HEIGHT // 2 - 40,
            100,
            50,
            "Легко",
            GREEN if self.selected_difficulty == "easy" else LIGHT_GRAY,
            (0, 255, 0) if self.selected_difficulty == "easy" else (220, 220, 220),
            FONT_SIZE_SMALL
        )
        
        self.medium_button = Button(
            WINDOW_WIDTH // 2 - 50,
            WINDOW_HEIGHT // 2 - 40,
            100,
            50,
            "Средне",
            GREEN if self.selected_difficulty == "medium" else LIGHT_GRAY,
            (0, 255, 0) if self.selected_difficulty == "medium" else (220, 220, 220),
            FONT_SIZE_SMALL
        )
        
        self.hard_button = Button(
            WINDOW_WIDTH // 2 + 50,
            WINDOW_HEIGHT // 2 - 40,
            100,
            50,
            "Сложно",
            GREEN if self.selected_difficulty == "hard" else LIGHT_GRAY,
            (0, 255, 0) if self.selected_difficulty == "hard" else (220, 220, 220),
            FONT_SIZE_SMALL
        )
        
        # Time selection dropdown
        time_options_labels = [f"{sec // 60} мин" for sec in TIME_OPTIONS]
        self.time_dropdown = Dropdown(
            WINDOW_WIDTH // 2 - 100,
            WINDOW_HEIGHT // 2 + 30,
            200,
            40,
            time_options_labels,
            TIME_OPTIONS.index(DEFAULT_GAME_DURATION)
        )
        
        self.confirm_settings_button = Button(
            WINDOW_WIDTH // 2 - 100,
            WINDOW_HEIGHT // 2 + 100,
            200,
            50,
            "Начать игру",
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
        
        self.edit_word_button = Button(
            WINDOW_WIDTH - 150, 
            150, 
            130, 40, 
            "Изменить", 
            BLUE, 
            (100, 150, 255),
            FONT_SIZE_SMALL
        )
        
        self.delete_word_button = Button(
            WINDOW_WIDTH - 150, 
            200, 
            130, 40, 
            "Удалить", 
            RED, 
            (255, 0, 0),
            FONT_SIZE_SMALL
        )
        
        self.save_word_button = Button(
            WINDOW_WIDTH - 150, 
            250, 
            130, 40, 
            "Сохранить", 
            GREEN, 
            (0, 255, 0),
            FONT_SIZE_SMALL
        )
        
        self.cancel_edit_button = Button(
            WINDOW_WIDTH - 150, 
            300, 
            130, 40, 
            "Отмена", 
            LIGHT_GRAY, 
            (220, 220, 220),
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
        
        self.difficulty_dropdown = Dropdown(
            50,
            150,
            200,
            40,
            ["easy", "medium", "hard"],
            1  # medium by default
        )
        
        self.word_list = WordList(
            50, 
            200, 
            WINDOW_WIDTH - 250, 
            WINDOW_HEIGHT - 270,
            self.word_manager.get_all_words()
        )
        
        self.message = ""
        self.message_timer = 0
        self.edit_mode = False
        self.word_being_edited = None
        
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
        self.current_screen = SCREEN_GAME
        self.time_left = self.selected_time
        self.start_time = time.time()
        self.end_time = self.start_time + self.time_left
        
        # Set difficulty for word manager
        self.word_manager.set_difficulty(self.selected_difficulty)
        
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
        self.edit_mode = False
        self.word_being_edited = None
        
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
        
    def enter_edit_mode(self, word, difficulty):
        """
        Enter edit mode for a word.
        
        Args:
            word (str): The word to edit
            difficulty (str): The difficulty level of the word
        """
        self.edit_mode = True
        self.word_being_edited = word
        self.word_input.set_text(word)
        self.difficulty_dropdown.set_selected_option(difficulty)
        
    def exit_edit_mode(self):
        """Exit edit mode."""
        self.edit_mode = False
        self.word_being_edited = None
        self.word_input.clear()
        
    def add_word(self):
        """Add a new word from the input field."""
        word = self.word_input.get_text().strip().lower()
        difficulty = self.difficulty_dropdown.get_selected_option()
        
        if not word:
            self.message = "Введите слово для добавления"
            self.message_timer = 180  # 3 seconds at 60 FPS
            return
            
        if self.word_manager.word_exists(word):
            self.message = f"Слово '{word}' уже существует"
            self.message_timer = 180
            return
            
        if self.word_manager.add_word(word, difficulty):
            self.message = f"Слово '{word}' добавлено"
            self.word_input.clear()
            # Refresh word list
            self.word_list.update_words(self.word_manager.get_all_words())
        else:
            self.message = "Ошибка при добавлении слова"
        self.message_timer = 180
        
    def update_word(self):
        """Update the word being edited."""
        if not self.word_being_edited:
            return
            
        new_word = self.word_input.get_text().strip().lower()
        difficulty = self.difficulty_dropdown.get_selected_option()
        
        if not new_word:
            self.message = "Введите слово"
            self.message_timer = 180
            return
            
        # If word hasn't changed, just update difficulty
        if new_word == self.word_being_edited:
            if self.word_manager.update_word(self.word_being_edited, new_word, difficulty):
                self.message = f"Слово '{new_word}' обновлено"
                self.exit_edit_mode()
                # Refresh word list
                self.word_list.update_words(self.word_manager.get_all_words())
            else:
                self.message = "Ошибка при обновлении слова"
        else:
            # Check if new word already exists
            if self.word_manager.word_exists(new_word):
                self.message = f"Слово '{new_word}' уже существует"
                self.message_timer = 180
                return
                
            if self.word_manager.update_word(self.word_being_edited, new_word, difficulty):
                self.message = f"Слово '{self.word_being_edited}' изменено на '{new_word}'"
                self.exit_edit_mode()
                # Refresh word list
                self.word_list.update_words(self.word_manager.get_all_words())
            else:
                self.message = "Ошибка при обновлении слова"
        self.message_timer = 180
        
    def delete_word(self):
        """Delete the selected word."""
        selected_info = self.word_list.get_selected_word_info()
        if not selected_info:
            self.message = "Выберите слово для удаления"
            self.message_timer = 180
            return
            
        word, _ = selected_info
        if self.word_manager.remove_word(word):
            self.message = f"Слово '{word}' удалено"
            self.word_list.clear_selection()
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
                self.time_dropdown.handle_event(event)
                
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self.easy_button.check_hover(mouse_pos)
                    self.medium_button.check_hover(mouse_pos)
                    self.hard_button.check_hover(mouse_pos)
                    self.confirm_settings_button.check_hover(mouse_pos)
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
                        elif self.confirm_settings_button.check_click(mouse_pos):
                            # Get selected time from dropdown
                            time_label = self.time_dropdown.get_selected_option()
                            # Convert label back to seconds
                            time_minutes = int(time_label.split()[0])
                            self.selected_time = time_minutes * 60
                            self.start_game()
                        elif self.back_from_difficulty_button.check_click(mouse_pos):
                            self.current_screen = SCREEN_MENU
                            
            elif self.current_screen == SCREEN_MANAGE:
                # Handle management screen events
                self.word_input.handle_event(event)
                self.difficulty_dropdown.handle_event(event)
                
                # Handle word list events
                action = self.word_list.handle_event(event)
                if action == "select":
                    # Show message with options when word is selected
                    self.message = "Выбрано слово. Нажмите 'Изменить' или 'Удалить'"
                    self.message_timer = 180
                
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self.back_button.check_hover(mouse_pos)
                    
                    if not self.edit_mode:
                        self.add_word_button.check_hover(mouse_pos)
                        self.edit_word_button.check_hover(mouse_pos)
                        self.delete_word_button.check_hover(mouse_pos)
                    else:
                        self.save_word_button.check_hover(mouse_pos)
                        self.cancel_edit_button.check_hover(mouse_pos)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        
                        if self.back_button.check_click(mouse_pos):
                            self.current_screen = SCREEN_MENU
                            
                        elif not self.edit_mode:
                            if self.add_word_button.check_click(mouse_pos):
                                self.add_word()
                            elif self.edit_word_button.check_click(mouse_pos):
                                selected_info = self.word_list.get_selected_word_info()
                                if selected_info:
                                    word, difficulty = selected_info
                                    self.enter_edit_mode(word, difficulty)
                                else:
                                    self.message = "Выберите слово для изменения"
                                    self.message_timer = 180
                            elif self.delete_word_button.check_click(mouse_pos):
                                self.delete_word()
                        else:
                            if self.save_word_button.check_click(mouse_pos):
                                self.update_word()
                            elif self.cancel_edit_button.check_click(mouse_pos):
                                self.exit_edit_mode()
                                
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
        title_text = self.large_font.render("Настройки игры", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4 - 40))
        self.screen.blit(title_text, title_rect)
        
        # Draw difficulty label
        difficulty_label = self.medium_font.render("Выберите сложность:", True, BLACK)
        self.screen.blit(difficulty_label, (WINDOW_WIDTH//2 - difficulty_label.get_width()//2, WINDOW_HEIGHT//2 - 80))
        
        # Draw difficulty description
        if self.selected_difficulty == "easy":
            desc_text = self.small_font.render("Легко: Простые слова", True, BLACK)
        elif self.selected_difficulty == "hard":
            desc_text = self.small_font.render("Сложно: Сложные слова", True, BLACK)
        else:  # medium
            desc_text = self.small_font.render("Средне: Слова средней сложности", True, BLACK)
            
        desc_rect = desc_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 10))
        self.screen.blit(desc_text, desc_rect)
        
        # Draw buttons
        self.easy_button.draw(self.screen)
        self.medium_button.draw(self.screen)
        self.hard_button.draw(self.screen)
        
        # Draw time label
        time_label = self.medium_font.render("Выберите время:", True, BLACK)
        self.screen.blit(time_label, (WINDOW_WIDTH//2 - time_label.get_width()//2, WINDOW_HEIGHT//2 + 5))
        
        # Draw time dropdown
        self.time_dropdown.draw(self.screen)
        
        # Draw confirm button
        self.confirm_settings_button.draw(self.screen)
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
        
        # Draw time info
        minutes = self.selected_time // 60
        time_text = self.small_font.render(f"Время: {minutes} минут", True, BLACK)
        time_rect = time_text.get_rect(center=(WINDOW_WIDTH//2, 260))
        self.screen.blit(time_text, time_rect)
        
        # Draw performance evaluation
        if self.score >= 15:
            evaluation_text = self.medium_font.render("Отличный результат! Вы мастер объяснений! 🏆", True, GREEN)
        elif self.score >= 10:
            evaluation_text = self.medium_font.render("Хороший результат! 👍", True, BLUE)
        elif self.score >= 5:
            evaluation_text = self.medium_font.render("Неплохо! Можно лучше 😊", True, BLACK)
        else:
            evaluation_text = self.medium_font.render("Практика делает мастера! Попробуйте ещё раз! 💪", True, RED)
            
        evaluation_rect = evaluation_text.get_rect(center=(WINDOW_WIDTH//2, 320))
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
        
        # Draw difficulty counts
        counts = self.word_manager.get_word_count_by_difficulty()
        counts_text = self.small_font.render(
            f"Легко: {counts.get('easy', 0)} | Средне: {counts.get('medium', 0)} | Сложно: {counts.get('hard', 0)}", 
            True, BLACK
        )
        self.screen.blit(counts_text, (50, 90))
        
        # Draw input field
        self.word_input.draw(self.screen)
        
        # Draw difficulty dropdown
        difficulty_label = self.small_font.render("Сложность:", True, BLACK)
        self.screen.blit(difficulty_label, (50, 130))
        self.difficulty_dropdown.draw(self.screen)
        
        # Draw buttons based on mode
        self.back_button.draw(self.screen)
        
        if not self.edit_mode:
            self.add_word_button.draw(self.screen)
            self.edit_word_button.draw(self.screen)
            self.delete_word_button.draw(self.screen)
        else:
            self.save_word_button.draw(self.screen)
            self.cancel_edit_button.draw(self.screen)
            # Show hint when in edit mode
            hint_text = self.small_font.render(f"Изменение: {self.word_being_edited}", True, (128, 128, 128))
            self.screen.blit(hint_text, (50, WINDOW_HEIGHT - 30))
        
        # Draw word list
        self.word_list.draw(self.screen)
        
        # Draw message if exists
        if self.message and self.message_timer > 0:
            message_color = RED if "Ошибка" in self.message or "уже существует" in self.message else GREEN
            if "Выбрано" in self.message:
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