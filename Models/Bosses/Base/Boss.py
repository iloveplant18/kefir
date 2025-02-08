import uuid

class Boss(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name, maxHp, level, rarity, expGain):
        self.id = uuid.uuid4
        self.name = name
        self.maxHp = maxHp
        self.hp = self.maxHp
        self.level = level
        self.rarity = rarity
        self.expGain = expGain
        self.usersDamage = dict()

    def GetHit(self, damage: int):
        self.hp -= damage

    def RefreshUserDamage(self, userId, hitpoints):
        if (userId in self.usersDamage.keys()):
            self.usersDamage[userId] += hitpoints
        else:
            self.usersDamage[userId] = hitpoints