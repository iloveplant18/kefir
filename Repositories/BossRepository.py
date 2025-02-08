from Models.Bosses.Base.Boss import Boss

# этот класс нужен для взаимодействия с данными о боссах. Пока он хранит private массив с боссами, в дальнейшем можно
# будет переделать его как захочется (например чтобы он в бд хранил данные)
# и на остальную прогу (например на BossService) это не повлияет, не придется там ниче переписывать
# главное сигнатуры методов не менять - типо что они возвращают и принимают.
# По хорошему интерфейс бы для этого написать


class BossRepository:

    _instance = None
    bosses = list()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def create(self, model) -> str or False :
        self.bosses.append(model)
        return model.id

    def get(self, bossId: int) -> Boss or None :
        return next((b for b in self.bosses if b.id == bossId), None)

    def delete(self, bossId) -> True :
        boss = self.get(bossId)
        if(boss is not None):
            self.bosses.remove(boss)
        return True

    def update(self, bossId, newValues: dict):
        boss = self.get(bossId)
        propertiesToUpdate = newValues.keys()
        for property in propertiesToUpdate:
            if hasattr(boss, property):
                setattr(boss, property, newValues[property])
            else:
                raise Exception('trying to update non existend property on boss')