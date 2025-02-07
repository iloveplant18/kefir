from config.bot_init import inject

class ChatEnemyService(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, chatId):
        self.chatEnemyRepository = inject._chatEnemyRepository