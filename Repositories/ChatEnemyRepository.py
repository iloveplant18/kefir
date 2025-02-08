from Models.ChatEnemy import ChatEnemy

class ChatEnemyRepository(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # Пока в переменной, но должна быть логика
    # работы с другими хранилищами
    chatEnemies = list()

    def get(self, chatId: int) -> ChatEnemy or None:
        return next((ce for ce in self.chatEnemies if ce.chatId == chatId), None)

    def create(self, model) -> str or None:

        if (next((ce for ce in self.chatEnemies if ce.chatId == model.chatId), None) is not None):
            return
        
        self.chatEnemies.append(model)

        return model.chatId
    
    def update(self, chatId: int, newValues: dict):

        chatEnemy = self.get(chatId)
        propertiesToUpdate = newValues.keys()

        for property in propertiesToUpdate:
            if hasattr(chatEnemy, property):
                setattr(chatEnemy, property, newValues[property])
            else:
                raise Exception('trying to update non existend property on character')
            
    def delete(self, chatId) -> True :
        chatEnemy = self.get(chatId)
        if(chatEnemy is not None):
            self.chatEnemies.remove(chatEnemy)
        return True