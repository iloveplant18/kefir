from Controllers.BossController import BossController
from Controllers.ChatEnemyController import ChatEnemyController
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


@bot.message_handler(commands=['boss'])
def start(message):
    
    chatEnemyController = ChatEnemyController(message.chat.id)
    enemyId = chatEnemyController.GetEnemyId()

    if(enemyId is not None):
        bot.send_message(message.chat.id, "Добейте этого")
        return
    
    bossController = BossController(message.chat.id, message.from_user.id, enemyId)
    bossId = bossController.spawnBoss()
    chatEnemyController.CreateEnemy(bossId)


@bot.message_handler(func=lambda message: message.text == "⚔ Ударить")
def hit(message):

    bot.delete_message(message.chat.id, message.id)

    chatEnemyController = ChatEnemyController(message.chat.id)
    enemyId = chatEnemyController.GetEnemyId()

    if(enemyId == None):
        bot.send_message(message.chat.id, "Бить некого.\nПиши /boss")
        return
    
    userDto = UserDto(message.from_user.id, message.from_user.first_name)

    characterController = CharacterController(message.chat.id, userDto.id)
    haveCharacter = characterController.CheckCharacter(userDto.id)

    if (haveCharacter == False):
        bot.send_message(message.chat.id, "Чтобы драться, нужен персонаж \nПиши /char")
        return

    characterController.DeleteLastOnCooldownMessage()
    onCooldown = characterController.CheckUserOnCooldown()

    if (onCooldown == True):
        characterController.SendAndSetOnCooldownMessage()
        return
    
    characterController.UnsetCooldown()
    characterController.DeleteHitAndCooldownMessages()

    bossController = BossController(message.chat.id, userDto.id, enemyId)
    damage = bossController.hitBoss(userDto)
    characterController.GoToCooldown()
    characterController.SendAndSetHitAndCooldownMessages(userDto, damage)

    isBossAlive = bossController.CheckIsBossAlive()

    if (isBossAlive == False):
        expCharactersDto = bossController.GetExperienceForCharacters()

        usersDamage = bossController.GetUsersDamage()
        bossController.KillBoss(usersDamage)
        chatEnemyController.Delete()

        characterController.GiveExperienceToCharacters(expCharactersDto)


@bot.message_handler(commands=['char'])
def showOrCreateCharacter(message):
    characterController = CharacterController(message.chat.id, message.from_user.id)
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