# В damageDTO вся информация о тычке персонажа
# У босса могут быть резисты к стихиям, броня и т.д.
# А у тычки персонажа могут быть характеристики,
# Позволяющие преодолеть сопротивления или заскейлить итоговый урон

class DamageDto:
    def __init__(self, hitpoints):
        self.hitpoints = hitpoints