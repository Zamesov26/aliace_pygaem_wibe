import random
import time
import threading
from datetime import timedelta


class Words:
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
        self.words = random.sample(self.words, len(self.words))

    def get_random_word(self):
        """Получает случайное слово из списка"""
        if not self.words:
            return None
        return self.words.pop()



class EliasGame:
    def __init__(self, word_manager: Words):
        # База слов для игры (можно расширить)
        self.word_manager = word_manager
        self.score = 0
        self.game_active = False
        self.time_delay = 10
        self.end_time = None
    
    
    def start_game(self):
        """Запускает игровой процесс"""
        start_time = time.time()
        self.end_time = start_time + self.time_delay
        print("=== ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'ЭЛИАС'! ===")
        print("Правила: у вас есть 2 минуты чтобы объяснять слова.")
        print("Команды:")
        print("  'y' + Enter - слово угадано (+1 очко)")
        print("  'n' + Enter - пропустить слово")
        print("  'quit' + Enter - закончить игру досрочно")
        print("\nНажмите Enter чтобы начать!")
        input()
        
        self.score = 0
        self.game_active = True
        
        # Запускаем таймер в отдельном потоке
        # Основной игровой цикл
        self.game_loop()
        
        # Завершение игры
        self.show_results()
    
    # def timer(self, seconds=120):
    #     """Отсчитывает время игры"""
    #     while  end_time > time.time():
    #         print("осталось времени", (end_time - time.time()), end="\r", flush=True)
    #         time.sleep(1)
    #
    #     self.game_active = False
    #     print("\n\nВремя вышло!")
    
    def game_loop(self):
        """Основной игровой цикл"""
        while time.time() < self.end_time:
            new_word = self.word_manager.get_random_word()
            if new_word is None:
                print("Все слова использованы!")
                print(f"Счёт: {self.score}")
                break
            
            print(f"Счёт: {self.score}")
            print(f"\nОбъясните слово: {new_word.upper()}")
            
            # Ждем ответа пользователя
            print("Угадано? (y/n/quit): ")
            user_input = input().strip().lower()
            
            if user_input == 'quit':
                self.game_active = False
                print("Игра завершена досрочно.")
                break
            elif user_input == 'y':
                self.score += 1
                print("✓ Верно! +1 очко")
            elif user_input == 'n':
                print("✗ Пропущено")
            else:
                print("Некорректный ввод. Слово пропущено.")
            
            # Небольшая пауза перед следующим словом
            time.sleep(0.5)
    
    def show_results(self):
        """Показывает результаты игры"""
        print("\n" + "=" * 40)
        print("ИГРА ОКОНЧЕНА!")
        print(f"Ваш итоговый счёт: {self.score}")
        
        # Простая оценка результата
        if self.score >= 15:
            print("Отличный результат! Вы мастер объяснений! 🏆")
        elif self.score >= 10:
            print("Хороший результат! 👍")
        elif self.score >= 5:
            print("Неплохо! Можно лучше 😊")
        else:
            print("Практика делает мастера! Попробуйте ещё раз! 💪")
            
# Запуск игры
if __name__ == "__main__":
    words = Words()
    game = EliasGame(words)
    
    # Можно добавить свои слова
    # game.add_words(["моё_слово", "ещё_слово"])
    
    game.start_game()
    
    # Предложение сыграть еще раз
    while True:
        again = input("\nХотите сыграть ещё раз? (y/n): ").lower()
        if again == 'y':
            game.start_game()
        elif again == 'n':
            print("Спасибо за игру! До свидания!")
            break
        else:
            print("Пожалуйста, введите 'y' или 'n'")