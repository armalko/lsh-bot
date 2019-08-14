import telebot
from telebot import types
bot = telebot.TeleBot("699738404:AAFNmDZck9wMMdJY9biysPjuMnQHAhNZHCg")

colour = 0
money = 0
name = ""
k = 0

@bot.message_handler(content_types=['text'])
def start(message):
    global k
    k = 0
    if message.text == '/start':
        str1 = "Вы выбираете один цвет - синий или оранжевый - и ставите на него определенную сумму. " \
               "Эту сумму надо вручную отправить через СИСТЕМУ на счёт 508 (Аксюткин Андрей). " \
               "Бот лишь помогает нам оптимизировать сбор данных. Ставить нужно ровно столько, сколько вы перевели. " \
               "Если суммы не совпадают, то учитывается та, которую вы перевели." \
               "Ставки всех участников суммируются и выигрывает цвет, сумма ставок на который меньше. " \
               "Поставившие на этот цвет объявляются победителями и им возвращается удвоенная ставка. " \
               "Те, кто поставили на другой цвет, проигрывают и не получают ничего."
        bot.send_message(message.from_user.id, str1)
        bot.send_message(message.from_user.id, "Отправь твой номер счета в ЛЭШ (только число)")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


def get_name(message):
    global name
    try:
        name = int(message.text)
        bot.send_message(message.from_user.id, "Введи сумму ставки!")
        bot.register_next_step_handler(message, get_money)
    except Exception:
        bot.send_message(message.from_user.id, "Такого счета нет. Начни сначала")


def get_money(message):
    global money
    try:
        money = int(message.text)
        keyboard = types.InlineKeyboardMarkup()
        key_blue = types.InlineKeyboardButton(text='синий', callback_data='blue')
        keyboard.add(key_blue)
        key_orange= types.InlineKeyboardButton(text='оранжевый', callback_data='orange')
        keyboard.add(key_orange)
        question = "Выбери цвет ставки!"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    except Exception:
        bot.send_message(message.from_user.id, "Такого числа нет. Пораааа все начинать с начала!")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global colour
    global k
    if call.data == "blue" and k == 0:
        colour = "blue"
        k+=1
        bot.send_message(call.message.chat.id, 'Ставка на синее успешно принята в обработку! Вы в игре!')
        f = open('datesofeverybody.txt', 'a')
        wr = str(name) + " added " + str(money) + " " + str(colour)
        f.write(wr + '\n')
        f.close()
    elif call.data == "orange" and k == 0:
        bot.send_message(call.message.chat.id, 'Ставка на оранжевое успешно принята в обработку! Вы в игре!')
        k+=1
        colour = "orange"
        f = open('datesofeverybody.txt', 'a')
        wr = str(name) + " added " + str(money) + " " + str(colour)
        f.write(wr + '\n')
        f.close()
    elif k >= 1:
        bot.send_message(call.message.chat.id, "Надо начать сначала( /start ?")


bot.polling(none_stop=True, interval=0)
