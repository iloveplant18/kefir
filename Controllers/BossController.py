import random

from Services.Shared.DateTimeOperationsService import DateTimeOperationsService
from Loggers.BossLogger import BossLogger
from Loggers.BattleLogger import BattleLogger
from Loggers.CharacterLogger import CharacterLogger
from Repositories.BossRepository import BossRepository
from Services.BossService import BossService
from Services.CharacterService import CharacterService
from config.bot_init import bot
from Services.CharacterService import TakeExpRequest
from DTOs.UsersDamageDto import UsersDamageDto


class BossController:

    usersOnCooldown     = dict()
    usersDamage         = dict()
    usersBlockedAttacks = list()

    def __init__(self, chatId):
        self.chatId           = chatId
        bossRepository        = BossRepository() # а если несколько боссов можно создать. Каждому свой репозиторий?
        bossLogger            = BossLogger(self.chatId)
        characterLogger       = CharacterLogger(self.chatId)
        self.battleLogger     = BattleLogger(self.chatId)
        self.bossService      = BossService(bossRepository, bossLogger, self.battleLogger)
        self.characterService = CharacterService(characterLogger)
        
    def spawnBoss(self):
        isBossExistsInChat = self.bossService.CheckIsBossExistsInChat(self.chatId)
        if (isBossExistsInChat):
            bot.send_message(self.chatId, "Вы че, добейте этого сначала")
            return

        self.bossService.SpawnBoss(self.chatId)

    def hitBoss(self, userDto):
        isBossExists = self.bossService.CheckIsBossExistsInChat(self.chatId)
        if (not isBossExists):
            bot.send_message(self.chatId, 'босс не призван, неполучится подраться эх')
            return
        
        if (self.CheckIsUserBlocked(userDto)):
            return
        self.BlockUser(userDto)

        if (self.CheckCooldown(userDto.id) == True):
            if(self.CheckReload(userDto.id, cooldownSeconds=15) == True):
                self.OutOfCooldown(userDto.id)
                self.battleLogger.CleanToCooldownLog(userDto.id)
                self.battleLogger.CleanHitLog(userDto.id)
            else:
                self.battleLogger.CleanLastCooldownLog()
                self.battleLogger.LogOnCooldown(userDto.name)
                self.UnblockUser(userDto)
                return
        
        # TODO Могут быть атаки мили, дальние, магические. У каждой свой метод
        damageDto = self.characterService.CalculateMeleeDamage(userDto.id)

        response = self.bossService.HitBoss(self.chatId, userDto, damageDto)
        self.RefreshUsersDamage(userDto.id, response.hitpoints)

        if (response.isEnemyAlive == False):
            exp = self.bossService.GetBossExpGain(self.chatId)
            usersDamageDtos = [UsersDamageDto(self.GetUserName(key), value) for key, value in self.usersDamage.items()]
            self.bossService.KillBoss(self.chatId, usersDamageDtos)
            for userId in self.usersDamage.keys():
                request = TakeExpRequest(userId, exp)
                self.characterService.TakeExp(request)
                self.UnblockUser(userDto)
            self.usersDamage.clear() #убрать когда решится проблема с неперезаписыванием контроллера в main
            return False

        self.GoToCooldown(userDto.id)
        self.battleLogger.LogToCooldown(userDto, cooldown=15)
        self.UnblockUser(userDto)
        return True

    def CheckIsUserBlocked(self, userDto):
        if (userDto.id in self.usersBlockedAttacks):
            return True
        else:
            return False
    
    def BlockUser(self, userDto):
        self.usersBlockedAttacks.append(userDto.id)

    def UnblockUser(self, userDto):
        self.usersBlockedAttacks.remove(userDto.id)

    def CheckCooldown(self, userId):
        usersOnCooldown = list(self.usersOnCooldown.keys())
        if (str(userId) in usersOnCooldown):
            return True
        else:
            return False
        
    def RefreshUsersDamage(self, userId, hitpoints):
        if (userId not in self.usersDamage.keys()):
             self.usersDamage[userId] = hitpoints
        else:
            self.usersDamage[userId] += hitpoints
        
    # В сервис персонажа
    def CheckReload(self, userId, cooldownSeconds):

        timeDeltaCooldown = DateTimeOperationsService.getTimeDeltaFromSeconds(cooldownSeconds)

        dateTimeNow = DateTimeOperationsService.getNowDateTime()
        dateTimeAttack = self.usersOnCooldown[f"{userId}"]

        timeDeltaLeft = dateTimeNow - dateTimeAttack

        if (timeDeltaLeft > timeDeltaCooldown):
            return True
        else:
            return False
        
    # В сервис персонажа
    def OutOfCooldown(self, userId):
        del self.usersOnCooldown[f"{userId}"]

    # В сервис персонажа
    def GoToCooldown(self, userId):
        dateTimeNow = DateTimeOperationsService.getNowDateTime()
        self.usersOnCooldown[f"{userId}"] = dateTimeNow
    
    def GetUserName(self, userId):
        user = bot.get_chat(userId)
        return user.first_name