from Loggers.CharacterLogger import CharacterLogger
from Repositories.CharacterRepository import CharacterRepository
from Services.CharacterService import CharacterService


class CharacterController:

    def __init__(self, chatId: int):
        self.chatId = chatId
        characterRepository = CharacterRepository()
        self.characterRepository = characterRepository
        characterLogger = CharacterLogger(chatId)
        self.characterService = CharacterService(characterRepository, characterLogger)

    def showOrCreate(self, userId: int, name: str, maxHp: int):
        character = self.characterRepository.get(userId)
        if (character):
            self.characterService.showCharacter(character)
        else:
            self.characterService.createCharacter(userId, name, maxHp)
