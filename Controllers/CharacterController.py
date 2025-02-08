from Services.CharacterService import CharacterService

class CharacterController:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, chatId: int, userId):
        self.chatId = chatId
        self.characterService = CharacterService(chatId, userId)


    def CheckCharacter(self, userId):
        character = self.characterService.GetCharacter(userId)

        if (character == None):
            return False
        else:
            return True

    def showOrCreate(self, userDto):

        haveCharacter = self.CheckCharacter(userDto.id)
        if (haveCharacter == True):
            self.characterService.showCharacter()
        else:
            self.characterService.createCharacter(userDto)


    def GiveExperienceToCharacters(self, expCharactersDto):
        for characterId in expCharactersDto.characterIds:
            self.characterService.TakeExp(characterId, expCharactersDto.exp)


    def DeleteLastOnCooldownMessage(self):
        self.characterService.DeleteLastOnCooldownMessage()


    def DeleteHitAndCooldownMessages(self):
        self.characterService.DeleteHitAndCooldownMessages()


    def SendAndSetOnCooldownMessage(self):
        self.characterService.SendAndSetOnCooldownMessage()


    def SendAndSetHitAndCooldownMessages(self, userDto, damage):
        self.characterService.SendAndSetHitAndCooldownMessages(userDto, damage)


    def CheckUserOnCooldown(self):

        onCooldown = self.characterService.CheckOnCooldown()

        if (onCooldown == True):
            isReloaded = self.characterService.CheckReload(cooldownSeconds=15)

            if (isReloaded == True):
                self.characterService.OutOfCooldown()
                return False
            else:
                return True
        else:
            return False


    def GoToCooldown(self):
        self.characterService.SetCooldown()

    
    def UnsetCooldown(self):
        self.characterService.SetCooldown()
            
    