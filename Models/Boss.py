class Boss(object):

    def __init__(self, hp: int):
        self.hp = hp

    def GetHit(self, damage: int):
        self.hp -= damage
        return self.hp
