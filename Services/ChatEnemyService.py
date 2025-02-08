from config.bot_init import inject
from Models.ChatEnemy import ChatEnemy

class ChatEnemyService(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, chatId):
        self.chatId = chatId
        self.chatEnemyRepository = inject._chatEnemyRepository

    def GetEnemyId(self):
        chatEnemy = self.chatEnemyRepository.get(self.chatId)

        if (chatEnemy == None):
            return None

        enemyId = chatEnemy.enemyId
        return enemyId
    
    def SaveEnemy(self, enemyId):
        chatEnemy = ChatEnemy(self.chatId, enemyId)
        self.chatEnemyRepository.create(chatEnemy)

    def Delete(self):
        self.chatEnemyRepository.delete(self.chatId)