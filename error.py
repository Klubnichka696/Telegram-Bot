import telebot
from telebot import types
import datetime

token = '7408355865:AAH8xWBc79ogwnUwwS3KrG-AZTtmvSCJzGU'
bot = telebot.TeleBot(token)
notes_dict = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Калькулятор', 'Заметки', 'Мем дня', 'Я соскучился по тебе')
    bot.send_message(message.chat.id, 'Привет! Я бот, который может выполнить несколько действий: \n1) Калькулятор; \n2) Заметки; \n3) Мем дня; \n4) Напиши, что ты соскучился по мне;', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Калькулятор')
def calculator_inline(message):
    bot.send_message(message.chat.id, 'Введите математическое выражение.')
    bot.register_next_step_handler(message, calculate)

def calculate(message):
    try:
        result = eval(message.text)
        bot.send_message(message.chat.id, f'Результат: {result}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')


@bot.message_handler(func=lambda message: message.text == 'Заметки')
def notes_inline(message):
    bot.send_message(message.chat.id, 'Напиши заметку или отправь "Показать заметки" чтобы просмотреть сохраненные заметки.')
    bot.register_next_step_handler(message, save_or_show_notes)

def save_or_show_notes(message):
    global notes_dict
    if message.text.lower() == 'показать заметки':
        notes = notes_dict.get(message.from_user.id, [])
        if notes:
            bot.send_message(message.chat.id, 'Сохраненные заметки:')
            for note in notes:
                bot.send_message(message.chat.id, f'• {note}')
        else:
            bot.send_message(message.chat.id, 'У вас нет сохраненных заметок.')
    else:
        note_text = message.text
        current_notes = notes_dict.get(message.from_user.id, [])
        current_notes.append(note_text)
        notes_dict[message.from_user.id] = current_notes
        bot.send_message(message.chat.id, 'Заметка сохранена.')


@bot.message_handler(func=lambda message: message.text == 'Мем дня')
def mem_inline(message):
    today = datetime.date.today()
    meme_url = f'https://picsum.photos/id/{today.day}/500/300'
    bot.send_message(message.chat.id, 'Вот мем дня:')
    bot.send_photo(message.chat.id, meme_url)

@bot.message_handler(func=lambda message: message.text == 'Я соскучился по тебе')
def icku_inline(message):
    bot.send_message(message.chat.id, 'Я тоже по тебе сокучился!!!')
    bot.send_photo(message.chat.id, '')

bot.infinity_polling()