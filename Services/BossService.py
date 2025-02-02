from Models.Boss import Boss
from Repositories.BossRepository import BossRepository
from Services.Shared.OperationsService import OperationsService
from telebot.types import ReplyKeyboardRemove
from datetime import datetime

class BossService(object):

    usersOnCooldown = dict()
    isBossAlive = True
    lastCDMessageId = None

    def __init__(self, bossRepository, logger):
        self.bossRepository = bossRepository
        self.logger = logger

    def SpawnBoss(self, chatId: int, hp: int) -> Boss or False :
        self.bossRepository.create(chatId, hp)
        self.logger.logSpawn(hp)

    def HitBoss(self, chatId, damage, damager):
        boss = self.bossRepository.get(chatId)
        boss.hp -= damage
        if boss.hp <= 0:
            self.KillBoss(chatId)
            return
        self.bossRepository.update(chatId, {
            "hp": boss.hp
        })
        self.logger.logHit(damager.name, damage, boss.hp)
        # userId = message.from_user.id
        # userName = message.from_user.first_name
        #
        # #порефакторить
        # usersOnCooldown = list(self.usersOnCooldown.keys())
        # if (str(userId) in usersOnCooldown):
        #     cooldown = datetime(2025, 2, 2, 0, 0, 30).time()
        #     cooldown = datetime.combine(datetime.min, cooldown)
        #
        #     time = datetime.now().time()
        #     time = datetime.combine(datetime.min, time)
        #
        #     timeLeft = time - self.usersOnCooldown[f"{userId}"]
        #     if (timeLeft > cooldown - datetime.min):
        #         self.OutOfCooldown(userId, userName)
        #     else:
        #         cDMessageId = self.bot.send_message(self.chatId, f'{userName}, ты кд')
        #         if(self.lastCDMessageId is not None):
        #             self.bot.delete_message(self.chatId, self.lastCDMessageId)
        #         self.lastCDMessageId = cDMessageId.id
        #         return
        #
        # hpAfterHit = self.boss.GetHit(damage)
        #
        # if (hpAfterHit <= 0):
        #     hpAfterHit = 0
        #     self.isBossAlive = False
        #
        # # BattleLogs.LogHit(self.chatId, self.bot, userName, damage, hpAfterHit)
        #
        # # self.GoToCooldown(userId, userName)
        #
        # return

    def KillBoss(self, chatId: int) -> None:
        self.bossRepository.delete(chatId)
        self.logger.logKill()

    def CheckIsBossExistsInChat(self, chatId) -> bool:
        bossInChat = self.bossRepository.get(chatId)
        return bool(bossInChat)

    # убрать из BossService
    # def OutOfCooldown(self, userId, userName):
    #     del self.usersOnCooldown[f"{userId}"]

    # убрать из BossService
    # def GoToCooldown(self, userId, userName):
    #     time = datetime.now().time()
    #     time = datetime.combine(datetime.min, time)
    #     self.usersOnCooldown[f"{userId}"] = time
    #     self.bot.send_message(self.chatId, f'{userName} в кд 30 секунд')

