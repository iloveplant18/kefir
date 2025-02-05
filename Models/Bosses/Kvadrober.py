from Models.Bosses.Base.Boss import Boss

class Kvadrober(Boss) : 
    def __init__(self):
        super().__init__(name="Квадробер-ебака",
                         hp=120,
                         level=1,
                         rarity="Обычный",
                         expGain=52)
        
    def GetHit(self, damage: int):
        super().GetHit(damage)