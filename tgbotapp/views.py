import copy
from django.shortcuts import render, redirect
from django.core.cache import cache
from . import terms_work
from . import vocab_db
from . import quiz
from . import models
from django.conf import settings
import random
import telebot
from telebot import types

bot = telebot.TeleBot(settings.KEY_TOKEN)

global quizzes
global languages
global adding


KeyboardButtons = ["Добавить новое слово",
                   "Посмотреть доступные слова",
                   "Посмотреть статискиту тестов",
                   "Изменить язык",
                   "Английский",
                   "Армянский",
                   "Другой язык",
                   ]


@bot.message_handler(commands=['start'])
def welcome(message):
    vocab_db.write_user(message.from_user.id)
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                     "бот-словарь для помощи в изучении <b>иностранного языка</b>.\n"
                     "Здесь Вы можете собирать, сохранять и изучать слова выбранного Вами языка.\n"
                     "Перед тем, как начать, выберите изучаемый язык с помощью команды /setlanguage "
                     "(можно менять в дальнейшем при желании).\n"
                     "Пользуйтесь <b>Меню</b> для навигации в боте.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')


@bot.message_handler(commands=['setlanguage'])
def setlanguage(message):

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(KeyboardButtons[4])
    item2 = types.KeyboardButton(KeyboardButtons[5])
    item3 = types.KeyboardButton(KeyboardButtons[6])
    markup.add(item1, item2, item3)
    global languages
    if 'languages' in globals():
        languages[message.from_user.id] = settings.NOT_CHOSEN
    else:
        languages = dict()
        languages[message.from_user.id] = settings.NOT_CHOSEN
    bot.send_message(message.chat.id,
                     "Выберите изучаемый язык*.\n\n"
                     "<i>* Другие языки пока не реализованы.</i>".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['quiz'])
def quiz_starter(message):
    if languages[message.from_user.id] == settings.NOT_CHOSEN:
        bot.send_message(message.chat.id, "Выберите язык перед тем как пройти квиз.")
    else:
        global quizzes
        if 'quizzes' in globals():
            quizzes[message.from_user.id] = quiz.Quiz(message.from_user.id, languages[message.from_user.id])
        else:
            quizzes = dict()
            quizzes[message.from_user.id] = quiz.Quiz(message.from_user.id, languages[message.from_user.id])

        term = quizzes[message.from_user.id].next_qna()[1]
        bot.send_message(message.chat.id, term)


@bot.message_handler(content_types=['text'])
def menu_handler(message):
    if message.text in KeyboardButtons:
        if message.text == KeyboardButtons[0]:
            global adding
            if 'adding' in globals():
                adding.append = ([message.from_user.id, 1, 0, 'newword', 'newtrans'])
            else:
                adding = []
                adding.append = ([message.from_user.id, 1, 0, 'newword', 'newtrans'])
            bot.send_message(message.chat.id, "Напишите новое слово.")
        elif message.text == KeyboardButtons[1]:
            results = []
            words = vocab_db.get_terms_for_table(languages[message.from_user.id])
            bot.send_message(message.chat.id, "У Вас {0} слов.".format(len(words)))
            for each in words:
                results.append(str(each[1]) + ' - ' + str(each[2]))
            ret = '\n'.join(results)
            bot.send_message(message.chat.id, ret)
        elif message.text == KeyboardButtons[2]:
            res = vocab_db.get_stats(message.from_user.id)
            stats = res[0]
            bot.send_message(message.chat.id,
                             "Ваша статистика:\n\n"
                             "Английский: {0} тестов, средний результат - {1}\n\n"
                             "Армянский: {2} тестов, средний результат - {3}"
                             .format(stats[1], stats[2], stats[3], stats[4]))
        elif message.text == KeyboardButtons[3]:
            bot.send_message(message.chat.id, "Для изменения языка используйте команду /setlanguage.")
        elif message.text == KeyboardButtons[4]:
            languages[message.from_user.id] = settings.ENGLISH
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton(KeyboardButtons[0])
            item2 = types.KeyboardButton(KeyboardButtons[1])
            item3 = types.KeyboardButton(KeyboardButtons[2])
            item4 = types.KeyboardButton(KeyboardButtons[3])

            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, "Выбран английский.\n"
                                              "Чем желаете заняться?",
                             reply_markup=markup)
        elif message.text == KeyboardButtons[5]:
            languages[message.from_user.id] = settings.ARMENIAN
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton(KeyboardButtons[0])
            item2 = types.KeyboardButton(KeyboardButtons[1])
            item3 = types.KeyboardButton(KeyboardButtons[2])
            item4 = types.KeyboardButton(KeyboardButtons[3])

            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, "Выбран армянский.\n"
                                              "Чем желаете заняться?",
                             reply_markup=markup)
        elif message.text == KeyboardButtons[6]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton(KeyboardButtons[4])
            item2 = types.KeyboardButton(KeyboardButtons[5])
            item3 = types.KeyboardButton(KeyboardButtons[6])
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id,
                             "Извините, других языков пока нет.\n"
                             "Пожалуйста, выберите один из имеющихся языков.".format(
                                 message.from_user, bot.get_me()),
                             parse_mode='html', reply_markup=markup)
    elif 'adding' in globals():
        for usssr in adding:
            if usssr[0] == message.from_user.id:
                if usssr[1] == 1:
                    usssr[3] = message.text
                    usssr[1] = 0
                    usssr[2] = 1
                    bot.send_message(message.chat.id, "Напишите перевод слова.")
                if usssr[2] == 1:
                    usssr[4] = message.text
                    vocab_db.write_term(usssr[3], usssr[4], message.from_user.id, languages[message.from_user.id])
                    adding.remove(usssr)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                    item1 = types.KeyboardButton(KeyboardButtons[0])
                    item2 = types.KeyboardButton(KeyboardButtons[1])
                    item3 = types.KeyboardButton(KeyboardButtons[2])
                    item4 = types.KeyboardButton(KeyboardButtons[3])

                    markup.add(item1, item2, item3, item4)
                    bot.send_message(message.chat.id, "Новое слово внесено.\n"
                                                      "Чем желаете заняться?",
                                     reply_markup=markup)
    elif 'quizzes' not in globals():
        bot.reply_to(message, 'Пользуйтесь меню для работы с ботом.')
    elif message.from_user.id not in quizzes:
        bot.reply_to(message, 'Пользуйтесь меню для работы с ботом.')
    else:
        try:
            term = quizzes[message.from_user.id].next_qna()[1]
            bot.send_message(message.chat.id, term)
            quizzes[message.from_user.id].record_user_answer(message.text)
        except StopIteration:
            quizzes[message.from_user.id].record_user_answer(message.text)
            mess, res = quizzes[message.from_user.id].check_quiz()
            results = " ".join(mess)
            vocab_db.update_stats(message.from_user.id, res, languages[message.from_user.id])
            bot.send_message(message.chat.id, results)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton(KeyboardButtons[0])
            item2 = types.KeyboardButton(KeyboardButtons[1])
            item3 = types.KeyboardButton(KeyboardButtons[2])
            item4 = types.KeyboardButton(KeyboardButtons[3])

            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, "Квиз закончен, результаты сохранены.\n"
                                              "Чем желаете заняться?",
                             reply_markup=markup)
            del quizzes[message.from_user.id]


bot.polling(non_stop=True)
