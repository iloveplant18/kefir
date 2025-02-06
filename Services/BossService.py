from Models.Bosses.Base.Boss import Boss
from Models.Bosses.Kvadrober import Kvadrober
from DTOs.BossInfoDto import BossInfoDto
from Models.Character import Character
from DTOs.AttackResponse import AttackResponse

class BossService(object):

    def __init__(self, bossRepository, bossLogger, battleLogger):
        self.bossRepository = bossRepository
        self.bossLogger = bossLogger
        self.battleLogger = battleLogger
        self.idBossInfoMessage = None

    def SpawnBoss(self, chatId: int) -> Boss or False :
        
        # Подумать как лучше реализовать создание любого босса по запросу
        boss = Kvadrober()
        self.bossRepository.create(chatId, boss)

        self.infoDto = BossInfoDto(boss.name, boss.level, boss.hp, boss.hp, boss.rarity)
        self.bossLogger.logSpawn()
        self.idBossInfoMessage = self.bossLogger.SendBossCard(self.infoDto)

    def HitBoss(self, chatId, userDto, damageDto):
        
        boss = self.bossRepository.get(chatId)
        
        # Логика расчета урона damage=... с учетом сопротивлений босса
        damage = damageDto.hitpoints # Пока заглушка

        boss.GetHit(damage)
        hpAfterHit = boss.hp

        if(hpAfterHit <= 0):
            response = AttackResponse(False, damage)
            return response

        updateRequest = { "hp": hpAfterHit }

        self.bossRepository.update(chatId, updateRequest)
        self.battleLogger.LogHit(userDto, damage)
        self.infoDto.hp = hpAfterHit
        self.battleLogger.RefreshEnemyInfo(self.idBossInfoMessage, self.infoDto)

        response = AttackResponse(True, damage)
        return response
        
    def KillBoss(self, chatId: int, usersDamageDtos) -> None:
        self.bossRepository.delete(chatId)
        self.bossLogger.RemoveBossCard(self.idBossInfoMessage)
        self.bossLogger.LogKill(self.infoDto, usersDamageDtos)

    def CheckIsBossExistsInChat(self, chatId) -> bool:
        bossInChat = self.bossRepository.get(chatId)
        return bool(bossInChat)

    def GetBossExpGain(self, chatId):
        boss = self.bossRepository.get(chatId)
        return boss.expGain
   
