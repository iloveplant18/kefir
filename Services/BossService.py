from Models.Bosses.Base.Boss import Boss
from Models.Bosses.Kvadrober import Kvadrober
from DTOs.BossInfoDto import BossInfoDto
from DTOs.ExpCharactersDto import ExpCharactersDto
from config.bot_init import inject
from Loggers.BattleLogger import BattleLogger
from Loggers.BossLogger import BossLogger

class BossService(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, chatId, enemyId):
        self.bossRepository = inject._bossRepository
        self.boss = self.GetBoss(enemyId)
        self.chatId = chatId
        self.bossLogger = BossLogger(chatId)
        self.battleLogger = BattleLogger(chatId)
        

    def GetBoss(self, enemyId):
        return self.bossRepository.get(enemyId)

    def SpawnBoss(self: int) -> Boss or False :
        
        # Подумать как лучше реализовать создание любого босса по запросу
        boss = Kvadrober()
        bossId = self.bossRepository.create(boss)

        self.bossLogger.logSpawn()

        infoDto = BossInfoDto(boss.name, boss.level, boss.hp, boss.maxHp, boss.rarity)
        self.idBossInfoMessage = self.bossLogger.SendBossCard(infoDto)

        return bossId


    def HitBoss(self, userDto, damageDto):
        
        # Логика расчета урона damage=... с учетом сопротивлений босса
        damage = damageDto.hitpoints # Пока заглушка

        if (self.boss.hp < damage):
            damage = self.boss.hp

        self.boss.GetHit(damage)
        self.boss.RefreshUserDamage(userDto.id, damage)

        updateRequest = { "hp": self.boss.hp, "usersDamage": self.boss.usersDamage}
        self.bossRepository.update(self.boss.id, updateRequest)

        infoDto = BossInfoDto(self.boss.name, self.boss.level, self.boss.hp, self.boss.maxHp, self.boss.rarity)
        self.battleLogger.RefreshEnemyInfo(self.idBossInfoMessage, infoDto)

        return damage


    def GetExperienceForCharacters(self):

        usersDamage = self.GetUsersDamage()
        exp = self.GetBossExpGain()

        characters = [id for id in usersDamage.keys()]
        expCharactersDto = ExpCharactersDto(exp, characters)

        return expCharactersDto
        
    def KillBoss(self, usersDamageDtos) -> None:
        self.bossRepository.delete(self.chatId)
        self.bossLogger.RemoveBossCard(self.idBossInfoMessage)
        self.bossLogger.LogKill(self.boss.name, usersDamageDtos)

    def CheckIsBossAlive(self):

        if (self.boss.hp > 0):
            return True
        else:
            return False

    def GetBossExpGain(self):
        if (self.boss is None):
            return None

        return self.boss.expGain
    
    def GetUsersDamage(self):
        if (self.boss is None):
            return None
        
        return self.boss.usersDamage

   
