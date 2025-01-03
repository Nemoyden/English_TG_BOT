import json
import os

class DataHandler:
    "Класс для работы с данными слов и пользователей"

    def __init__(self, data_file='data.json', users_file='users.json'):
        self.data_file = data_file
        self.users_file = users_file
        self.load_data()
        self.load_users()

    def load_data(self):
        "Загружаем банки слов из файла"
        if not os.path.exists(self.data_file):
            self.data = {'easy': [], 'medium': [], 'hard': []}
            self.save_data()
        else:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

    def save_data(self):
        "Сохраняем банки слов в файл"
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_users(self):
        "Загружаем данные пользователя"
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
        "Добавляем слово в банк"
        if difficulty in self.data:
            self.data[difficulty].append({'word': word, 'translation': translation})
            self.save_data()

    def get_random_word(self, difficulty):
        "Получаем случайное слово из банка по сложности"
        import random
        if self.data[difficulty]:
            return random.choice(self.data[difficulty])
        else:
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
