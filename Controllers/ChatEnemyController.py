from Services.ChatEnemyService import ChatEnemyService

class ChatEnemyController:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, chatId: int):
        self.chatId = chatId
        self.chatEnemyService = ChatEnemyService(chatId)
    
    def GetEnemyId(self):
        return self.chatEnemyService.GetEnemyId()
    
    def CreateEnemy(self, enemyId):
        self.chatEnemyService.SaveEnemy(enemyId)

    def Delete(self):
        self.chatEnemyService.Delete()
