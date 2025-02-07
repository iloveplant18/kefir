from Models.Bosses.Base.Boss import Boss
from Models.Bosses.Kvadrober import Kvadrober
from DTOs.BossInfoDto import BossInfoDto
from DTOs.AttackResponse import AttackResponse
from config.bot_init import inject
from Loggers.BattleLogger import BattleLogger
from Loggers.BossLogger import BossLogger

class BossService(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, chatId):
        self.chatId = chatId
        self.bossLogger = BossLogger(chatId)
        self.battleLogger = BattleLogger(chatId)
        self.idBossInfoMessage = None
        self.bossRepository = inject._bossRepository

    def SpawnBoss(self: int) -> Boss or False :
        
        # Подумать как лучше реализовать создание любого босса по запросу
        boss = Kvadrober()
        self.bossRepository.create(self.chatId, boss)

        self.infoDto = BossInfoDto(boss.name, boss.level, boss.hp, boss.hp, boss.rarity)
        self.bossLogger.logSpawn()
        self.idBossInfoMessage = self.bossLogger.SendBossCard(self.infoDto)

    def HitBoss(self, userDto, damageDto):
        
        boss = self.bossRepository.get(self.chatId)
        
        # Логика расчета урона damage=... с учетом сопротивлений босса
        damage = damageDto.hitpoints # Пока заглушка
        damage = 70

        boss.GetHit(damage)
        hpAfterHit = boss.hp

        if(hpAfterHit <= 0):
            response = AttackResponse(False, damage)
            return response

        updateRequest = { "hp": hpAfterHit }

        self.bossRepository.update(self.chatId, updateRequest)
        self.battleLogger.LogHit(userDto, damage)
        self.infoDto.hp = hpAfterHit
        self.battleLogger.RefreshEnemyInfo(self.idBossInfoMessage, self.infoDto)

        response = AttackResponse(True, damage)
        return response
        
    def KillBoss(self, usersDamageDtos) -> None:
        self.bossRepository.delete(self.chatId)
        self.bossLogger.RemoveBossCard(self.idBossInfoMessage)
        self.bossLogger.LogKill(self.infoDto, usersDamageDtos)

    def CheckIsBossExistsInChat(self) -> bool:
        bossInChat = self.bossRepository.get(self.chatId)
        return bool(bossInChat)

    def GetBossExpGain(self):
        boss = self.bossRepository.get(self.chatId)
        return boss.expGain
   
