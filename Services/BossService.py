from Models.Bosses.Base.Boss import Boss
from Models.Bosses.Kvadrober import Kvadrober
from DTOs.BossInfoDto import BossInfoDto

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

    def HitBoss(self, chatId, userDto, damageDto): # damage нужно будет убрать. Брать урон из character
        
        boss = self.bossRepository.get(chatId)
        
        # Логика расчета урона damage=... 
        damage = damageDto.hitpoints # Пока заглушка
        
        boss.GetHit(damage)
        hpAfterHit = boss.hp

        if (hpAfterHit <= 0): # Эта логика должна переехать
            hpAfterHit = 0
            self.KillBoss(chatId)
            return
        else:
            updateRequest = { "hp": hpAfterHit }

            self.bossRepository.update(chatId, updateRequest)
            self.battleLogger.LogHit(userDto.name, damage)
            self.infoDto.hp = hpAfterHit
            self.battleLogger.RefreshEnemyInfo(self.idBossInfoMessage, self.infoDto)

            return
        
    def KillBoss(self, chatId: int) -> None:
        self.bossRepository.delete(chatId)
        self.bossLogger.LogKill()

    def CheckIsBossExistsInChat(self, chatId) -> bool:
        bossInChat = self.bossRepository.get(chatId)
        return bool(bossInChat)


   
