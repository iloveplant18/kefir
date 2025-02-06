from Controllers.BossController import BossController
from Controllers.CharacterController import CharacterController
from DTOs.UserDto import UserDto
from config.bot_init import bot
from Services.AcheService import AcheService, IcheService, RandomUntilConversationService
from telebot.types import BotCommand, BotCommandScopeChat
import os


bot.set_my_commands([
    BotCommand("char", "Создать персонажа"),
    BotCommand("boss", "Призвать босса"),
])
scope=BotCommandScopeChat(chat_id=os.getenv('BOT_KEY'))
bossControllers = dict()


@bot.message_handler(commands=['boss'])
def start(message):
    # это нужно отрефакторить
    if (message.chat.id not in bossControllers.keys()):
        bossControllers[message.chat.id] = BossController(message.chat.id) # оно не перезаписывает объект 
    bossControllers[message.chat.id].spawnBoss()

@bot.message_handler(func=lambda message: message.text == "⚔ Ударить")#has_character=True)
def hit(message):
    userDto = UserDto(message.from_user.id, message.from_user.first_name)
    bossController = bossControllers[message.chat.id]
    bot.delete_message(message.chat.id, message.id)
    if (bossController.characterService.CheckCharacter(userDto.id) == False):
        bot.send_message(message.chat.id, "Чтобы драться, нужен персонаж \nПиши /char")
        return
    result = bossController.hitBoss(userDto)
    if (result == False):
        del bossControllers[message.chat.id]


@bot.message_handler(commands=['char'])
def showOrCreateCharacter(message):
    characterController = CharacterController(message.chat.id)
    userDto = UserDto(message.from_user.id, message.from_user.first_name)
    characterController.showOrCreate(userDto)


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