from Models.Bosses.Base.Boss import Boss

class Kvadrober(Boss):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        super().__init__(name="Квадробер-ебака",
                         maxHp=120,
                         level=1,
                         rarity="Обычный",
                         expGain=52)
        
    def GetHit(self, damage: int):
        super().GetHit(damage)