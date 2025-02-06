import random

# У персонажа те характеристики, которые будут расти с уровнем
class Character(object):
    
    def __init__(self, 
                 userId, 
                 name):
        self.userId = userId
        self.name = name
        self.level = 1
        self.exp = 0
        self.expNeed = 100
        self.maxHp = 20
        self.hp = self.maxHp
        self.damageBase = 5
        self.armor = 0 
        self.elementalResistance = 0

    def TakeExp(self, exp):
        self.exp += exp

    def CheckLevelUp(self):
        if (self.exp >= self.expNeed):
            return True
        else:
            return False

    def LevelUp(self):
        self.level += 1
        self.exp -= self.expNeed
        self.expNeed = self.expNeed + 30
        self.maxHp = int(self.maxHp * 1.1)
        self.damageBase += random.randint(1, 2)
        self.armor += random.randint(0, 1)
        self.elementalResistance += 1

    def HealFull(self):
        self.hp = self.maxHp

    def GetMeleeDamageMinMax(self):

        minBaseDamage = self.damageBase - int(self.damageBase*0.2)
        maxBaseDamage = self.damageBase + int(self.damageBase*0.2)

        return minBaseDamage, maxBaseDamage

