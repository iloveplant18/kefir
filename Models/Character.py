
class Character:
    def __init__(self, userId, name, maxHp):
        self.userId = userId
        self.name = name
        self.maxHp = maxHp
        self.hp = self.maxHp
