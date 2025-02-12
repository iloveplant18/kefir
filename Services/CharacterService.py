from Models.Character import Character
from DTOs.DamageDto import DamageDto
from DTOs.CharacterDto import CharacterInfoDto
from DTOs.UserDto import UserDto
from config.bot_init import inject
from Services.CharacterMessageService import CharacterMessageService
from Services.BattleMessageService import BattleMessageService
from Services.Shared.DateTimeOperationsService import DateTimeOperationsService
import random

class CharacterService(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, chatId, userId):
        self.characterRepository = inject._characterRepository
        self.chatId = chatId
        self.characterMessageService = CharacterMessageService(chatId)
        self.battleMessageService = BattleMessageService(chatId)
        self.character = self.GetCharacter(userId)

    def showCharacter(self):
        character = self.character

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

        self.characterMessageService.logStats(characterInfoDto)

    def createCharacter(self, userDto) -> Character or None:

        character = Character(userDto.id, userDto.name)
        
        self.characterRepository.create(character)
        self.characterMessageService.logCreation(userDto.name)

    def TakeExp(self, userId, exp):
        character = self.characterRepository.get(userId)

        character.TakeExp(exp)

        if (character.CheckLevelUp() == True):
            character.LevelUp()
            self.characterMessageService.LogLevelUp(character.name)
        
        request = dict({"level": character.level, 
                        "exp":  character.exp,
                        "expNeed": character.expNeed,
                        "maxHp": character.maxHp,
                        "damageBase": character.damageBase,
                        "armor": character.armor,
                        "elementalResistance": character.elementalResistance
                        })

        self.characterRepository.update(character.userId, request)


    def CalculateMeleeDamage(self):
        character = self.character

        dmgBaseRange = character.GetMeleeDamageMinMax()  
        damageBase = random.randint(dmgBaseRange[0], dmgBaseRange[1])

        #... Прибавление урона от вещей + пробивающие способности
        damageDto = DamageDto(hitpoints=damageBase)

        return damageDto

    
    def CheckCharacter(self):
        character = self.character

        if (character is None):
            return False
        else:
            return True
        
    def CheckOnCooldown(self):

        onCooldown = self.character.onCooldown

        if (onCooldown == True):
            return True
        else:
            return False


    def CheckReload(self, cooldownSeconds):
        character = self.character

        timeDeltaCooldown = DateTimeOperationsService.getTimeDeltaFromSeconds(cooldownSeconds)

        dateTimeNow = DateTimeOperationsService.getNowDateTime()
        dateTimeAttack = character.lastAttackDateTime

        timeDeltaLeft = dateTimeNow - dateTimeAttack

        if (timeDeltaLeft > timeDeltaCooldown):
            return True
        else:
            return False
        

    def OutOfCooldown(self):
        self.character.onCooldown = False
        self.characterRepository.update(self.character.userId, {"onCooldown": self.character.onCooldown})

        
    def GetCharacter(self, userId):
        return self.characterRepository.get(userId)
    

    def DeleteLastOnCooldownMessage(self):
       self.characterMessageService.DeleteOnCooldownMessage(self.character.userId)
            

    def DeleteHitAndCooldownMessages(self):
        self.characterMessageService.DeleteHitAndCooldownMessages(self.character.userId)


    def SendAndSetOnCooldownMessage(self):
        character = self.character

        userDto = UserDto(character.userId, character.name)

        self.battleMessageService.LogOnCooldown(userDto)


    def SendAndSetHitAndCooldownMessages(self, userDto, damage):
        self.battleMessageService.LogHit(userDto, damage)
        self.battleMessageService.LogToCooldown(userDto, cooldown=15)


    def SetCooldown(self):
        character = self.character

        dateTimeNow = DateTimeOperationsService.getNowDateTime()
        character.lastAttackDateTime = dateTimeNow

        character.onCooldown = True

        self.characterRepository.update(character.userId, {"lastAttackDateTime": character.lastAttackDateTime, "onCooldown": character.onCooldown})

    
    def UnsetCooldown(self):
        character = self.character

        character.lastAttackDateTime = None

        self.characterRepository.update(character.userId, {"lastAttackDateTime": character.lastAttackDateTime})