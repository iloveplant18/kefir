from Loggers.CharacterLogger import CharacterLogger
from Services.CharacterService import CharacterService

class CharacterController:

    def __init__(self, chatId: int):
        self.chatId = chatId
        self.characterService = CharacterService(chatId)

    def showOrCreate(self, userDto):
        haveCharacter = self.characterService.CheckCharacter(userDto.id)
        if (haveCharacter):
            self.characterService.showCharacter(userDto.id)
        else:
            self.characterService.createCharacter(userDto)