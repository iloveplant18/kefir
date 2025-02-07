from Models.Character import Character
from DTOs.DamageDto import DamageDto
from DTOs.CharacterDto import CharacterInfoDto
from config.bot_init import inject
from Loggers.CharacterLogger import CharacterLogger
import random

# Перенести
class TakeExpRequest:
    def __init__(self, characterId, exp):
        self.characterId = characterId
        self.exp = exp

class CharacterService(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, chatId):
        self.chatId = chatId
        self.characterRepository = inject._characterRepository
        self.logger = CharacterLogger(chatId)

    def showCharacter(self, userId):

        character = self.characterRepository.get(userId)
        meleeDmg = character.GetMeleeDamageMinMax()

        characterInfoDto = CharacterInfoDto(character.userId, 
                                            character.name, 
                                            character.level,
                                            character.exp,
                                            character.expNeed,
                                            character.maxHp, 
                                            meleeDmg[0],
                                            meleeDmg[1],
                                            0, 0, 0, 0, 0, #TODO Нужны методы расчета
                                            character.armor,
                                            character.elementalResistance)

        self.logger.logStats(characterInfoDto)

    def createCharacter(self, userDto) -> Character or None:
        self.characterRepository.create(userDto.id, userDto.name)
        self.logger.logCreation(userDto.name)

    def TakeExp(self, takeExpRequest : TakeExpRequest):

        character = self.characterRepository.get(takeExpRequest.characterId)

        character.TakeExp(takeExpRequest.exp)

        if (character.CheckLevelUp() == True):
            character.LevelUp()
            self.logger.LogLevelUp(character.name)
        
        request = dict({"level": character.level, 
                        "exp":  character.exp,
                        "expNeed": character.expNeed,
                        "maxHp": character.maxHp,
                        "damageBase": character.damageBase,
                        "armor": character.armor,
                        "elementalResistance": character.elementalResistance
                        })

        self.characterRepository.update(character.userId, request)

    def CalculateMeleeDamage(self, userId):

        character = self.characterRepository.get(userId)
        dmgBaseRange = character.GetMeleeDamageMinMax()  
        damageBase = random.randint(dmgBaseRange[0], dmgBaseRange[1])

        #... Прибавление урона от вещей + пробивающие способности
        damageDto = DamageDto(hitpoints=damageBase)

        return damageDto
    
    def CheckCharacter(self, userId):
        if (self.characterRepository.checkIsCharacterExists(userId)):
            return True
        else:
            return False

    
        
        
        
        
        

