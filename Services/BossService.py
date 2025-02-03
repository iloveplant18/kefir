from Models.Boss import Boss

class BossService(object):

    def __init__(self, bossRepository, bossLogger, battleLogger):
        self.bossRepository = bossRepository
        self.bossLogger = bossLogger
        self.battleLogger = battleLogger


    def SpawnBoss(self, chatId: int, hp: int) -> Boss or False :
        self.bossRepository.create(chatId, hp)
        self.bossLogger.logSpawn(hp)

    def HitBoss(self, chatId, userDto, damageDto): # damage нужно будет убрать. Брать урон из character
        
        boss = self.bossRepository.get(chatId)

        # Логика расчета урона damage=... 
        damage = damageDto.hitpoints # Пока заглушка
        
        hpAfterHit = boss.GetHit(damage)
        
        
        if (hpAfterHit <= 0): # Эта логика должна переехать
            hpAfterHit = 0
            self.KillBoss(chatId)
            return
        else:
            updateRequest = { "hp": hpAfterHit }

            self.bossRepository.update(chatId, updateRequest)
            self.battleLogger.LogHit(userDto.name, damage, hpAfterHit)

            return
        
    def KillBoss(self, chatId: int) -> None:
        self.bossRepository.delete(chatId)
        self.bossLogger.LogKill()

    def CheckIsBossExistsInChat(self, chatId) -> bool:
        bossInChat = self.bossRepository.get(chatId)
        return bool(bossInChat)


   
