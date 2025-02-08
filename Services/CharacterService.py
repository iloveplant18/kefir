from Models.Character import Character
from DTOs.DamageDto import DamageDto
from DTOs.CharacterDto import CharacterInfoDto
from config.bot_init import inject
from Loggers.CharacterLogger import CharacterLogger
from Loggers.BattleLogger import BattleLogger
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
        self.logger = CharacterLogger(chatId)
        self.battleLogger = BattleLogger(chatId)
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

        self.logger.logStats(characterInfoDto)

    def createCharacter(self, userDto) -> Character or None:

        character = Character(userDto.id, userDto.name)

        #Удалить в новой версии
        for i in range(15):
            character.LevelUp()
        character.exp = 0
        
        self.characterRepository.create(character)
        self.logger.logCreation(userDto.name)

    def TakeExp(self, userId, exp):
        character = self.characterRepository.get(userId)

        character.TakeExp(exp)

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
        character = self.character

        if (character.onCooldown == True):
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
        character = self.character

        character.onCooldown = False
        self.characterRepository.update(character.userId, {"onCooldown": character.onCooldown}) # смешная штука. реалии текущей репы
        

    def GetCharacter(self, userId):
        return self.characterRepository.get(userId)
    

    def DeleteLastOnCooldownMessage(self):
        character = self.character

        messageId = character.lastOnCooldownMessageId

        if (messageId == None):
            return
        
        character.lastOnCooldownMessageId = None

        self.characterRepository.update(character.userId, {"lastOnCooldownMessageId": character.lastOnCooldownMessageId})

        self.logger.DeleteMessage(messageId)

    def DeleteHitAndCooldownMessages(self):
        character = self.character

        hitMessageId = character.lastHitMessageId
        cooldownMessageId = character.lastCooldownMessageId

        if (hitMessageId is None or cooldownMessageId is None):
            return
        
        character.lastHitMessageId = None
        character.lastCooldownMessageId = None

        self.characterRepository.update(character.userId, {"lastHitMessageId": character.lastHitMessageId, "lastCooldownMessageId": character.lastCooldownMessageId})

        self.logger.DeleteMessage(hitMessageId)
        self.logger.DeleteMessage(cooldownMessageId)


    def SendAndSetOnCooldownMessage(self):
        character = self.character

        userName = character.name
        onCooldownMessageId = self.battleLogger.LogOnCooldown(userName)

        character.lastOnCooldownMessageId = onCooldownMessageId

        self.characterRepository.update(character.userId, {"lastOnCooldownMessageId": character.lastOnCooldownMessageId})


    def SendAndSetHitAndCooldownMessages(self, userDto, damage):
        character = self.character

        hitMessageId = self.battleLogger.LogHit(userDto, damage)
        cooldownMessageId = self.battleLogger.LogToCooldown(userDto, cooldown=15)

        character.lastHitMessageId = hitMessageId
        character.lastCooldownMessageId = cooldownMessageId

        self.characterRepository.update(character.userId, {"lastHitMessageId": character.lastHitMessageId, "lastCooldownMessageId": character.lastCooldownMessageId})
    

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