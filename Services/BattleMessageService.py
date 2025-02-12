from config.bot_init import bot, inject
from Services.Shared.OperationsService import OperationsService
from Services.BossMessageService import BossMessageService
from Models.Message import Message

class BattleMessageService(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, chatId):
            self.chatId = chatId
            self.messageRepository = inject._messageRepository
            self.bossMessageService = BossMessageService(chatId)


    hitPhrases = [
        '👊 {name} въебал на {damage} урона',
        '👊 {name}: Тычка {damage} урона'
    ]


    def LogHit(self, userDto, damage):
        phrase = OperationsService.GetShuffledAnswer(self.hitPhrases)
        response = phrase.format(damage=damage, name=userDto.name)
        messageId = bot.send_message(self.chatId, response).id

        message = Message(messageId, response, isHitMessage=True, userId=userDto.id)

        self.messageRepository.create(message)


    def RefreshEnemyInfo(self, bossInfoDto):
        response = self.bossMessageService.bossCard.format(name=bossInfoDto.name,
                                    level=bossInfoDto.level,
                                    hp=bossInfoDto.hp,
                                    maxhp=bossInfoDto.maxhp,
                                    rarity=bossInfoDto.rarity)
        
        message = self.messageRepository.getBossCard()

        if (message == None):
             return
        else:
                bot.edit_message_text(chat_id=self.chatId, message_id=message.id, text=response, parse_mode="Markdown")
            # вообще в репе сейчас респонс не обновляется, кто хотите пофиксите

        
    def LogOnCooldown(self, userDto):
        phrase = f"{userDto.name}, ты кд" #добавить сколько времени осталось
        messageId = bot.send_message(self.chatId, phrase).id

        message = Message(messageId, None, isOnCooldownMessage=True, userId=userDto.id)

        self.messageRepository.create(message)


    def LogToCooldown(self, userDto, cooldown):
        phrase = f'⌛ {userDto.name} в кд {cooldown} секунд'
        messageId = bot.send_message(self.chatId, phrase).id
        
        message = Message(messageId, None, isCooldownMessage=True, userId=userDto.id)

        self.messageRepository.create(message)

    def DeleteAllGameMessages(self):
        messages = self.messageRepository.getAll()

        #избавиться бы от try catch
        for message in messages:
            try:
                bot.delete_message(self.chatId, message.id)
                self.messageRepository.delete(message.id)
            except:
                self.messageRepository.delete(message.id)
                continue
            
