import random

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from Loggers.BossLogger import BossLogger
from Repositories.BossRepository import BossRepository
from Repositories.CharacterRepository import CharacterRepository
from Services.BossService import BossService
from Services.CharacterService import CharacterService
from Services.Shared.OperationsService import OperationsService
from config.bot_init import bot


class BossController:
    def __init__(self, chatId):
        self.chatId = chatId

        bossRepository = BossRepository()
        bossLogger = BossLogger(self.chatId)
        bossService = BossService(bossRepository, bossLogger)
        self.bossService = bossService


    def spawnBoss(self):

        isBossExistsInChat = self.bossService.CheckIsBossExistsInChat(self.chatId)
        if (isBossExistsInChat):
            bot.send_message(self.chatId, "Вы че, добейте этого сначала")
            return

        self.bossService.SpawnBoss(self.chatId, random.randint(60, 80))

    def hitBoss(self, userId):
        isBossExists = self.bossService.CheckIsBossExistsInChat(self.chatId)
        if (not isBossExists):
            bot.send_message(self.chatId, 'босс не призван, неполучится подраться эх')
            return

        # TODO: проверка возможно ли ударить босса (есть ли кулдаун или чета такое)

        characterRepository = CharacterRepository()
        character = characterRepository.get(userId)
        self.bossService.HitBoss(self.chatId, random.randint(1, 8), character)
