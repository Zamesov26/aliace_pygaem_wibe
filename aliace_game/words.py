"""
Word management for the Elias game.
This module handles the word list and provides functionality for getting random words.
"""

import random
from .database import WordDatabase

class Words:
    """Manages the word list for the game using SQLite database."""
    
    def __init__(self, db_path="words.db"):
        """
        Initialize the word manager with words from database.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db = WordDatabase(db_path)
        self.words = self.db.get_random_words()

    def get_random_word(self):
        """
        Получает случайное слово из списка.
        Returns a random word from the list or None if all words have been used.
        """
        if not self.words:
            return None
        return self.words.pop()
    
    def add_word(self, word):
        """
        Add a new word to the database.
        
        Args:
            word (str): The word to add
            
        Returns:
            bool: True if successful, False if word already exists
        """
        success = self.db.add_word(word)
        if success:
            # Refresh the words list
            self.words = self.db.get_random_words()
        return success
    
    def remove_word(self, word):
        """
        Remove a word from the database.
        
        Args:
            word (str): The word to remove
            
        Returns:
            bool: True if successful, False if word not found
        """
        success = self.db.remove_word(word)
        if success:
            # Refresh the words list
            self.words = self.db.get_random_words()
        return success
    
    def get_all_words(self):
        """
        Get all words from the database.
        
        Returns:
            list: List of all words
        """
        return self.db.get_all_words()
    
    def word_exists(self, word):
        """
        Check if a word exists in the database.
        
        Args:
            word (str): The word to check
            
        Returns:
            bool: True if word exists, False otherwise
        """
        return self.db.word_exists(word)
    
    def get_word_count(self):
        """
        Get the total number of words in the database.
        
        Returns:
            int: Number of words in the database
        """
        return self.db.get_word_count()