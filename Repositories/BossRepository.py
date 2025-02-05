from Models.Bosses.Base.Boss import Boss

# этот класс нужен для взаимодействия с данными о боссах. Пока он хранит private массив с боссами, в дальнейшем можно
# будет переделать его как захочется (например чтобы он в бд хранил данные)
# и на остальную прогу (например на BossService) это не повлияет, не придется там ниче переписывать
# главное сигнатуры методов не менять - типо что они возвращают и принимают.
# По хорошему интерфейс бы для этого написать
bosses = dict()

class BossRepository:

    def create(self, chatId: int, model) -> Boss or False :
        if chatId in bosses:
            return False
        bosses[chatId] = model # второй босс перезапишет первого. А если хотим создать несколько боссов? -> делать боссам айди
        return bosses[chatId]

    def get(self, chatId: int) -> Boss or None :
        if chatId in bosses:
            return bosses[chatId]

    def delete(self, chatId: int) -> bool :
        isBossExistsInChat = self.get(chatId)
        if not isBossExistsInChat:
            return False
        del bosses[chatId]
        return True

    def update(self, chatId: int, newValues: dict):
        boss = self.get(chatId)
        propertiesToUpdate = newValues.keys()
        for property in propertiesToUpdate:
            if hasattr(boss, property):
                setattr(boss, property, newValues[property])
            else:
                raise Exception('trying to update non existend property on boss')
