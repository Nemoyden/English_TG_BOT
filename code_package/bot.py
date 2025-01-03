import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
)
from .data_handler import DataHandler
from .scheduler import Scheduler
from .exceptions import DataLoadException
from .utils import generate_options
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('7818925498:AAHow4WrE15u5JmN7MBOP_gDKvGB5Bnh5BI')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

data_handler = DataHandler()

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Я бот для изучения английских слов. Пожалуйста, выберите уровень сложности:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Простой", callback_data='set_difficulty_easy')],
            [InlineKeyboardButton("Средний", callback_data='set_difficulty_medium')],
            [InlineKeyboardButton("Сложный", callback_data='set_difficulty_hard')]
        ])
    )

def set_difficulty(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    difficulty = query.data.split('_')[-1]
    context.user_data['difficulty'] = difficulty
    send_quiz(context.bot, query.message.chat_id, difficulty)

def send_quiz(bot, chat_id, difficulty=None):
    if not difficulty:
        difficulty = 'easy'  
    word_entry = data_handler.get_random_word(difficulty)
    if not word_entry:
        bot.send_message(chat_id, "Извините, нет слов в выбранной категории.")
        return
    correct_translation = word_entry['translation']
    all_translations = [w['translation'] for w_list in data_handler.data.values() for w in w_list if w['translation'] != correct_translation]
    options = generate_options(correct_translation, all_translations)
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"answer_{opt}_{correct_translation}")] for opt in options]
    bot.send_message(
        chat_id,
        f"Как переводится слово '{word_entry['word']}'?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def handle_answer(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    selected_translation = query.data.split('_')[1]
    correct_translation = query.data.split('_')[2]
    if selected_translation == correct_translation:
        query.edit_message_text("Верно! Отличная работа!")
    else:
        query.edit_message_text(f"Неправильно. Правильный ответ: {correct_translation}")

def add_word(update: Update, context: CallbackContext):
    try:
        _, word, translation = update.message.text.split(' ', 2)
        data_handler.add_word('user_words', word, translation)
        update.message.reply_text(f"Слово '{word}' добавлено в ваш банк слов.")
    except ValueError:
        update.message.reply_text("Пожалуйста, используйте формат: /add слово перевод")

def set_quiz_time(update: Update, context: CallbackContext):
    try:
        _, time_str = update.message.text.strip().split(' ')
        data_handler.set_user_quiz_time(update.effective_user.id, time_str)
        update.message.reply_text(f"Время ежедневного квиза установлено на {time_str}.")
    except ValueError:
        update.message.reply_text("Пожалуйста, используйте формат: /set_time ЧЧ:ММ")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('add', add_word))
    dispatcher.add_handler(CommandHandler('set_time', set_quiz_time))
    dispatcher.add_handler(CallbackQueryHandler(set_difficulty, pattern='set_difficulty_.*'))
    dispatcher.add_handler(CallbackQueryHandler(handle_answer, pattern='answer_.*'))

    scheduler = Scheduler(updater, data_handler)
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
