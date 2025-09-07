"""
Database module for the Elias game.
This module handles all SQLite database operations for word management.
"""

import sqlite3
import os
import random
from contextlib import contextmanager

class WordDatabase:
    """Handles SQLite database operations for words."""
    
    def __init__(self, db_path="words.db"):
        """
        Initialize the database connection.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize the database with the required tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if the words table exists and has the difficulty column
            cursor.execute("PRAGMA table_info(words)")
            columns = [info[1] for info in cursor.fetchall()]
            
            if 'difficulty' not in columns:
                # Add difficulty column if it doesn't exist
                cursor.execute("ALTER TABLE words ADD COLUMN difficulty TEXT DEFAULT 'medium'")
            else:
                # Create the table with all columns if it doesn't exist
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS words (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        word TEXT NOT NULL UNIQUE,
                        difficulty TEXT DEFAULT 'medium',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            
            conn.commit()
            
            # Insert default words if the table is empty
            cursor.execute("SELECT COUNT(*) FROM words")
            count = cursor.fetchone()[0]
            if count == 0:
                default_words = [
                    ("компьютер", "medium"), ("программа", "medium"), ("алгоритм", "hard"), 
                    ("библиотека", "medium"), ("функция", "medium"),
                    ("переменная", "medium"), ("цикл", "medium"), ("условие", "medium"), 
                    ("список", "easy"), ("словарь", "medium"),
                    ("модуль", "medium"), ("класс", "hard"), ("объект", "hard"), 
                    ("интерфейс", "hard"), ("база данных", "hard"),
                    ("сервер", "hard"), ("клиент", "medium"), ("интернет", "easy"), 
                    ("браузер", "easy"), ("сайт", "easy"),
                    ("приложение", "medium"), ("игра", "easy"), ("графика", "medium"), 
                    ("анимация", "medium"), ("звук", "easy"),
                    ("файл", "easy"), ("папка", "easy"), ("система", "hard"), 
                    ("безопасность", "hard"), ("пароль", "medium"),
                    ("кофе", "easy"), ("телефон", "easy"), ("солнце", "easy"), 
                    ("книга", "easy"), ("ручка", "easy"),
                    ("окно", "easy"), ("дверь", "easy"), ("стол", "easy"), 
                    ("стул", "easy"), ("лампа", "easy")
                ]
                cursor.executemany("INSERT INTO words (word, difficulty) VALUES (?, ?)", 
                                 default_words)
                conn.commit()
    
    def add_word(self, word, difficulty="medium"):
        """
        Add a new word to the database.
        
        Args:
            word (str): The word to add
            difficulty (str): The difficulty level (easy, medium, hard)
            
        Returns:
            bool: True if successful, False if word already exists
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO words (word, difficulty) VALUES (?, ?)", (word, difficulty))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # Word already exists
            return False
    
    def remove_word(self, word):
        """
        Remove a word from the database.
        
        Args:
            word (str): The word to remove
            
        Returns:
            bool: True if successful, False if word not found
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM words WHERE word = ?", (word,))
            conn.commit()
            return cursor.rowcount > 0
    
    def update_word(self, old_word, new_word, difficulty):
        """
        Update a word in the database.
        
        Args:
            old_word (str): The current word
            new_word (str): The new word
            difficulty (str): The difficulty level
            
        Returns:
            bool: True if successful, False if error occurred
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE words SET word = ?, difficulty = ? WHERE word = ?", 
                             (new_word, difficulty, old_word))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # New word already exists
            return False
    
    def get_all_words(self):
        """
        Get all words from the database.
        
        Returns:
            list: List of all words with their difficulties
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT word, difficulty FROM words ORDER BY word")
            return [(row[0], row[1]) for row in cursor.fetchall()]
    
    def get_words_by_difficulty(self, difficulty):
        """
        Get words by difficulty level.
        
        Args:
            difficulty (str): The difficulty level (easy, medium, hard)
            
        Returns:
            list: List of words with the specified difficulty
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT word FROM words WHERE difficulty = ? ORDER BY RANDOM()", (difficulty,))
            return [row[0] for row in cursor.fetchall()]
    
    def get_random_words(self, difficulty=None):
        """
        Get words in random order, optionally filtered by difficulty.
        
        Args:
            difficulty (str, optional): The difficulty level (easy, medium, hard)
            
        Returns:
            list: List of words in random order
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if difficulty:
                cursor.execute("SELECT word FROM words WHERE difficulty = ? ORDER BY RANDOM()", (difficulty,))
            else:
                cursor.execute("SELECT word FROM words ORDER BY RANDOM()")
            return [row[0] for row in cursor.fetchall()]
    
    def word_exists(self, word):
        """
        Check if a word exists in the database.
        
        Args:
            word (str): The word to check
            
        Returns:
            bool: True if word exists, False otherwise
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM words WHERE word = ?", (word,))
            return cursor.fetchone() is not None
    
    def get_word_info(self, word):
        """
        Get information about a specific word.
        
        Args:
            word (str): The word to look up
            
        Returns:
            tuple: (word, difficulty) or None if not found
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT word, difficulty FROM words WHERE word = ?", (word,))
            row = cursor.fetchone()
            return (row[0], row[1]) if row else None
    
    def get_word_count(self):
        """
        Get the total number of words in the database.
        
        Returns:
            int: Number of words in the database
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM words")
            return cursor.fetchone()[0]
    
    def get_word_count_by_difficulty(self):
        """
        Get the count of words by difficulty level.
        
        Returns:
            dict: Dictionary with difficulty levels as keys and counts as values
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT difficulty, COUNT(*) FROM words GROUP BY difficulty")
            return {row[0]: row[1] for row in cursor.fetchall()}