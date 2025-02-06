from Loggers.CharacterLogger import CharacterLogger
from Services.CharacterService import CharacterService

class CharacterController:

    def __init__(self, chatId: int):
        self.chatId = chatId
        characterLogger = CharacterLogger(chatId)
        self.characterService = CharacterService(characterLogger)

    def showOrCreate(self, userDto):
        haveCharacter = self.characterService.CheckCharacter(userDto.id)
        if (haveCharacter):
            self.characterService.showCharacter(userDto.id)
        else:
            self.characterService.createCharacter(userDto)