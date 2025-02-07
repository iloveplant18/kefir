from Repositories.ChatEnemyRepository import ChatEnemyRepository
from Repositories.BossRepository import BossRepository
from Repositories.CharacterRepository import CharacterRepository

class Inject():

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # Здесь регистрируем репозитории
    _chatEnemyRepository = ChatEnemyRepository()
    _bossRepository      = BossRepository()
    _characterRepository = CharacterRepository()

