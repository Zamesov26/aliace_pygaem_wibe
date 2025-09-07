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
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            
            # Insert default words if the table is empty
            cursor.execute("SELECT COUNT(*) FROM words")
            count = cursor.fetchone()[0]
            if count == 0:
                default_words = [
                    "компьютер", "программа", "алгоритм", "библиотека", "функция",
                    "переменная", "цикл", "условие", "список", "словарь",
                    "модуль", "класс", "объект", "интерфейс", "база данных",
                    "сервер", "клиент", "интернет", "браузер", "сайт",
                    "приложение", "игра", "графика", "анимация", "звук",
                    "файл", "папка", "система", "безопасность", "пароль",
                    "кофе", "телефон", "солнце", "книга", "ручка",
                    "окно", "дверь", "стол", "стул", "лампа"
                ]
                cursor.executemany("INSERT INTO words (word) VALUES (?)", 
                                 [(word,) for word in default_words])
                conn.commit()
    
    def add_word(self, word):
        """
        Add a new word to the database.
        
        Args:
            word (str): The word to add
            
        Returns:
            bool: True if successful, False if word already exists
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO words (word) VALUES (?)", (word,))
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
    
    def get_all_words(self):
        """
        Get all words from the database.
        
        Returns:
            list: List of all words
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT word FROM words ORDER BY word")
            return [row[0] for row in cursor.fetchall()]
    
    def get_random_words(self):
        """
        Get all words in random order.
        
        Returns:
            list: List of all words in random order
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
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