import random

from Services.Shared.DateTimeOperationsService import DateTimeOperationsService
from Loggers.BossLogger import BossLogger
from Loggers.BattleLogger import BattleLogger
from Repositories.BossRepository import BossRepository
from Repositories.CharacterRepository import CharacterRepository
from Services.BossService import BossService
from DTOs.DamageDto import DamageDto
from config.bot_init import bot


class BossController:

    usersOnCooldown = dict()

    def __init__(self, chatId):
        self.chatId = chatId

        bossRepository = BossRepository() # а если несколько боссов можно создать. Каждому свой репозиторий?
        bossLogger = BossLogger(self.chatId)
        self.battleLogger = BattleLogger(self.chatId)
        bossService = BossService(bossRepository, bossLogger, self.battleLogger)
        self.bossService = bossService

    def spawnBoss(self):

        isBossExistsInChat = self.bossService.CheckIsBossExistsInChat(self.chatId)
        if (isBossExistsInChat):
            bot.send_message(self.chatId, "Вы че, добейте этого сначала")
            return

        self.bossService.SpawnBoss(self.chatId, random.randint(60, 80))

    def hitBoss(self, userDto):
        isBossExists = self.bossService.CheckIsBossExistsInChat(self.chatId)
        if (not isBossExists):
            bot.send_message(self.chatId, 'босс не призван, неполучится подраться эх')
            return

        # TODO: проверка возможно ли ударить босса (есть ли кулдаун или чета такое)

        characterRepository = CharacterRepository() #Постоянно доставать одних и тех же челеков?
        character = characterRepository.get(userDto.id)

        if (self.CheckCooldown(userDto.id) == True):
            if(self.CheckReload(userDto.id, cooldownSeconds=30) == True):
                self.OutOfCooldown(userDto.id)

        # Двойная проверка специально, надо будет кое что потестить
        if (self.CheckCooldown(userDto.id) == True):
            self.battleLogger.CleanLastCooldownLog()
            self.battleLogger.LogOnCooldown(userDto.name)
            return
        
        # Брать damageDto из метода атаки персонажа
        damageDto = DamageDto(random.randint(1, 8))

        self.bossService.HitBoss(self.chatId, userDto, damageDto) 

        self.GoToCooldown(userDto.id)
        self.battleLogger.LogToCooldown(userDto.name, cooldown=30)

    def CheckCooldown(self, userId):
        usersOnCooldown = list(self.usersOnCooldown.keys())
        if (str(userId) in usersOnCooldown):
            return True
        else:
            return False
        

        
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
