import telebot
from Services.Depression import Depression
from Services.FiftyTwo import FiftyTwo
from Services.Yaaa import Yaaa


bot = telebot.TeleBot('7558145877:AAGws19U9dzRaR-LdsdQvNw1aEeKCBeQwCU')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'ПОГНАЛИ НАХУЙ ЙОБАНЫЙ В РОТ')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Спасибо, мне не нужна ваша помощь')

@bot.message_handler()
def answer_to_depression(message):
    depression = Depression()
    depressionAnswer = depression.handle_message(message.text)
    if (depressionAnswer):
        bot.send_message(message.chat.id, depressionAnswer)
        return

    fifty_two = FiftyTwo()
    answer = fifty_two.handle_message(message.text)
    if (answer):
        bot.send_message(message.chat.id, answer)

    yaaa = Yaaa()
    answer = yaaa.handle_message(message.text)
    if (answer):
        bot.send_message(message.chat.id, answer)


bot.polling(non_stop=True)