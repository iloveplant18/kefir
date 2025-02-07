from Repositories.ChatEnemyRepository import ChatEnemyRepository
from config.bot_init import inject

class ChatEnemyService(object):

    def __init__(self, logger):
        self.chatEnemyRepository = inject._chatEnemyRepository
        self.logger = logger