"""
Word management for the Elias game.
This module handles the word list and provides functionality for getting random words.
"""

import random

class Words:
    """Manages the word list for the game."""
    
    words = [
        "компьютер", "программа", "алгоритм", "библиотека", "функция",
        "переменная", "цикл", "условие", "список", "словарь",
        "модуль", "класс", "объект", "интерфейс", "база данных",
        "сервер", "клиент", "интернет", "браузер", "сайт",
        "приложение", "игра", "графика", "анимация", "звук",
        "файл", "папка", "система", "безопасность", "пароль",
        "кофе", "телефон", "солнце", "книга", "ручка",
        "окно", "дверь", "стол", "стул", "лампа"
    ]
    
    def __init__(self):
        """Initialize the word manager with a shuffled list of words."""
        self.words = random.sample(self.words, len(self.words))

    def get_random_word(self):
        """
        Получает случайное слово из списка.
        Returns a random word from the list or None if all words have been used.
        """
        if not self.words:
            return None
        return self.words.pop()