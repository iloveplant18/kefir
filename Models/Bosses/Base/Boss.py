class Boss(object):

    def __init__(self, name, hp, level, rarity, expGain):
        self.name = name
        self.hp = hp
        self.level = level
        self.rarity = rarity
        self.expGain = expGain

    def GetHit(self, damage: int):
        self.hp -= damage