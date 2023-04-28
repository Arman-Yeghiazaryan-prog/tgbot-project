from django.shortcuts import render

import telebot
import random
from botproject.settings import KEY_TOKEN
from telebot import types

bot = telebot.TeleBot(KEY_TOKEN)

KeyboardButton1 = "Добавить слово"
KeyboardButton2 = "Добавить учебный материал"
KeyboardButton3 = "Посмотреть доступные слова"
KeyboardButton4 = "Посмотреть доступные учебные материалы"


@bot.message_handler(commands=['start'])
def welcome(message):

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(KeyboardButton1)
    item2 = types.KeyboardButton(KeyboardButton2)
    item3 = types.KeyboardButton(KeyboardButton3)
    item4 = types.KeyboardButton(KeyboardButton4)

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                     "бот для помощи в изучении <i>иностранного языка</i>.\n"
                     "Здесь Вы можете собирать и сохранить изученные слова и "
                     "полезные материалы для обучения."
                     "Пользуйтесь <b>меню</b> для навигации в боте.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def menu_handler(message):
    if message.chat.type == 'private':
        if message.text == KeyboardButton1:
            bot.send_message(message.chat.id, "Expected to add new word, also {0}".format(str(random.randint(0, 100))))
        elif message.text == KeyboardButton2:
            bot.send_message(message.chat.id, "Expected to add learning material!")
        elif message.text == KeyboardButton3:
            bot.send_message(message.chat.id, "Show all saved words!")
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("To learn", callback_data='withdef')
            item2 = types.InlineKeyboardButton("To test myself", callback_data='nodef')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, "Choose the format.", reply_markup=markup)
        elif message.text == KeyboardButton4:
            bot.send_message(message.chat.id, "Show learning material with links.")
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'withdef':
                bot.send_message(call.message.chat.id, "No words for now")
            elif call.data == 'nodef':
                bot.send_message(call.message.chat.id, "No word here either")

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Sorry about that...",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="I'll add everything, I promise!")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)

