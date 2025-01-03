import json
import os
import random

class DataHandler:
    "Класс для работы с данными слов и пользователей"
    def __init__(self, words_file='words.json', users_file='users.json'):
        self.words_file = words_file
        self.users_file = users_file
        self.load_words()
        self.load_users()

    def load_words(self):
        "Загружаем банки слов из файла words.json"
        if not os.path.exists(self.words_file):
            self.data = {'easy': [], 'medium': [], 'hard': []}
            self.save_words()
        else:
            with open(self.words_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

    def save_words(self):
        "Сохраняем банки слов в файл words.json"
        with open(self.words_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_users(self):
        "Загружаем данные пользователей"
        if not os.path.exists(self.users_file):
            self.users = {}
            self.save_users()
        else:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)

    def save_users(self):
        "Сохраняем данные пользователей"
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)

    def add_word(self, difficulty, word, translation):
        "Добавляем слово в банк и сохраняем в файл words.json"
        if difficulty in self.data:
            for entry in self.data[difficulty]:
                if entry['word'] == word:
                    print(f"Слово '{word}' уже существует в категории '{difficulty}'.")
                    return
            
            self.data[difficulty].append({'word': word, 'translation': translation})
            self.save_words()
            print(f"Слово '{word}' добавлено в категорию '{difficulty}'.")

    def get_random_word(self, difficulty):
        "Получаем случайное слово из банка по сложности"
        if difficulty in self.data and self.data[difficulty]:
            return random.choice(self.data[difficulty])
        return None

    def set_user_quiz_time(self, user_id, time_str):
        "Устанавливаем время ежедневного квиза для пользователя"
        self.users[str(user_id)] = time_str
        self.save_users()

    def get_user_quiz_time(self, user_id):
        "Получаем время ежедневного квиза для пользователя"
        return self.users.get(str(user_id), None)

    def get_all_users(self):
        "Получаем список всех пользователей"
        return self.users.keys()

    def input_new_word(self):
        "Запрашивает у пользователя ввод нового слова и его перевода"
        difficulty = input("Введите уровень сложности (easy, medium, hard): ").strip().lower()
        if difficulty not in self.data:
            print("Некорректный уровень сложности. Пожалуйста, попробуйте снова.")
            return
        
        word = input("Введите новое слово: ").strip()
        translation = input("Введите перевод: ").strip()
        
        self.add_word(difficulty, word, translation)

    def get_quiz_question(self, difficulty):
        "Возвращает слово и варианты ответов для квиза"
        word_entry = self.get_random_word(difficulty)
        if not word_entry:
            return None, []
        
        correct_translation = word_entry['translation']
        options = [correct_translation]

        # Находим другие слова для создания вариантов ответа
        all_words = [entry['translation'] for entries in self.data.values() for entry in entries]
        while len(options) < 4:
            random_translation = random.choice(all_words)
            if random_translation not in options:  
                options.append(random_translation)

        random.shuffle(options)  
        return word_entry['word'], options
