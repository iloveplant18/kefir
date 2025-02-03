from Controllers.BossController import BossController
from Controllers.CharacterController import CharacterController
from Repositories.CharacterRepository import CharacterRepository
from config.bot_init import bot
from Services.AcheService import AcheService, IcheService, RandomUntilConversationService
from Services.BossService import BossService
import random
import threading
import config.register_filters
from telebot.types import BotCommand, ReplyKeyboardMarkup, KeyboardButton, BotCommandScopeChat
import os


bot.set_my_commands([
    BotCommand("battles", "В боевой режим"),
    BotCommand("chill", "В мирный режим"),
    BotCommand("boss", "Призвать босса"),
],
scope=BotCommandScopeChat(chat_id=os.getenv('BOT_KEY')))

@bot.message_handler(commands=['boss'])
def start(message):
    bossController = BossController(message.chat.id)
    bossController.spawnBoss()

@bot.message_handler(func=lambda message: message.text == "⚔ Ударить", has_character=True)
def hit(message):
    bossController = BossController(message.chat.id)
    bossController.hitBoss(message.from_user.id)

@bot.message_handler(commands=['character'])
def showOrCreateCharacter(message):
    characterController = CharacterController(message.chat.id)
    characterController.showOrCreate(message.from_user.id, message.from_user.first_name, 20)


@bot.message_handler(depression_filter=True)
def depression_controller(message):
    bot.reply_to(message, 'заплачь')

@bot.message_handler()
def message_handler(message):
    service = AcheService()
    response = service.Handle(message.text)
    if response:
        bot.send_message(message.chat.id, response)
        return

    service = IcheService()
    response = service.Handle(message.text)
    if (response):
        bot.send_message(message.chat.id, response)
        return

    # Случайная фраза прокает с определенным шансом на каждое сообщение
    service = RandomUntilConversationService()
    response = service.Handle(message.text)
    if (response):
        bot.send_message(message.chat.id, response)
        return


bot.infinity_polling()  