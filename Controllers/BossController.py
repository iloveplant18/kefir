from Loggers.BattleLogger import BattleLogger
from Services.CharacterService import CharacterService
from Services.BossService import BossService
from DTOs.UsersDamageDto import UsersDamageDto
from config.bot_init import bot


class BossController:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, chatId, userId, enemyId):
        self.chatId           = chatId
        self.battleLogger     = BattleLogger(self.chatId)
        self.bossService      = BossService(chatId, enemyId)
        self.characterService = CharacterService(chatId, userId)
        
    def spawnBoss(self):
        return self.bossService.SpawnBoss()

    def hitBoss(self, userDto):

        # TODO Могут быть атаки мили, дальние, магические. У каждой свой метод
        damageDto = self.characterService.CalculateMeleeDamage()

        damage = self.bossService.HitBoss(userDto, damageDto)

        return damage
        
    
    def GetUsersDamage(self):
        return self.bossService.GetUsersDamage()


    def GetExperienceForCharacters(self):
        return self.bossService.GetExperienceForCharacters()


    def CheckIsBossAlive(self):
        return self.bossService.CheckIsBossAlive()


    def KillBoss(self, usersDamage):
        usersDamageDtos = [UsersDamageDto(self.GetUserName(key), value) for key, value in usersDamage.items()]
        self.bossService.KillBoss(usersDamageDtos)


    def GetUserName(self, userId):
        chat = bot.get_chat(userId)
        return chat.first_name