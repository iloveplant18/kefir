from Services.Shared.OperationsService import OperationsService

class BossService(object):

    def __init__(self):
        self.spawnPhrases = [
            'Босс заспавнен, у него {bossHp} здоровья', 
            'Я вызвал босса, чуваки, у него {bossHp} здоровья'
        ]

        self.hitPhrases = [
            'Въебал на {damage} урона. У лоха осталось {bossHp} хп', 
            'Тычка {damage} урона, еще {bossHp} хп'
        ]

        self.killPhrases = [
            'Чмошный развалился, лут в след обновлениях (сосите)', 
            'Ну вы крутые, мужики, он всё. лут в след обновлениях (сосите)'
        ]

    def SpawnBoss(self, hp):
        self.boss = Boss(hp)
        phrase = OperationsService.GetShuffledAnswer(self.spawnPhrases)
        response = phrase.format(bossHp=self.boss.hp)
        return response
    
    def HitBoss(self, damage):
        hpAfterHit = self.boss.GetHit(damage)
        phrase = OperationsService.GetShuffledAnswer(self.hitPhrases)
        response = phrase.format(damage=damage, bossHp=hpAfterHit)

        if (hpAfterHit <= 0):
            response += "\n"
            response += OperationsService.GetShuffledAnswer(self.killPhrases)
            return response, True
        else:
            return response, False


class Boss(object):

    def __init__(self, hp):
        self.hp = hp

    def GetHit(self, damage):
        self.hp -= damage
        return self.hp

    

