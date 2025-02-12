from config.bot_init import bot, inject
from Models.Message import Message

class CharacterMessageService(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, chatId):
        self.chatId = chatId
        self.messageRepository = inject._messageRepository

    characterCard = "🦸‍♂️ **Игрок: {name}**\n" \
                    "📊 Уровень:  {level} ({exp} / {expNeed})\n\n" \
                    "Характеристики:\n" \
                    "❤️ Здоровье: {hp} HP\n" \
                    "⚔️ Физ. урон ближний: {minMeleeDmg} - {maxMeleeDmg}\n" \
                    "🏹 Физ. урон дальний: {minRangeDmg} - {maxRangeDmg}\n" \
                    "🔮 Маг. урон дальний: {minMagicDmg} - {maxMagicDmg}\n" \
                    "🌱 Сила лечения: {healPower}\n\n" \
                    "🛡️ Броня: {armor}\n" \
                    "💫 Маг. сопротивление: {elementalResistance}\n" \
    
    

    def logStats(self, characterInfoDto):
        response = self.characterCard.format(name=characterInfoDto.name,
                                        level=characterInfoDto.level,
                                        exp=characterInfoDto.exp,
                                        expNeed=characterInfoDto.expNeed,
                                        hp=characterInfoDto.hp,
                                        minMeleeDmg=characterInfoDto.minMeleeDmg,
                                        maxMeleeDmg=characterInfoDto.maxMeleeDmg,
                                        minRangeDmg=characterInfoDto.minRangeDmg,
                                        maxRangeDmg=characterInfoDto.maxRangeDmg,
                                        minMagicDmg=characterInfoDto.minMagicDmg,
                                        maxMagicDmg=characterInfoDto.maxMagicDmg,
                                        healPower=characterInfoDto.healPower,
                                        armor=characterInfoDto.armor,
                                        elementalResistance=characterInfoDto.elementalResistance,)
        
        messageId = bot.send_message(self.chatId, response, parse_mode="Markdown").id

        message = Message(messageId, None)
        self.messageRepository.create(message)


    def logCreation(self, userName):
        message =  f"{userName}, твой персонаж создан.\n" \
                    "Смотреть статы: /char\n" \
                    "Смортреть шмот: /inv"
        messageId = bot.send_message(self.chatId, message).id

        message = Message(messageId, None)
        self.messageRepository.create(message)


    def LogLevelUp(self, userName):
        message =  f"{userName}, ты повысил уровень\n"
        messageId = bot.send_message(self.chatId, message).id

        message = Message(messageId, None)

        self.messageRepository.create(message)


    def DeleteOnCooldownMessage(self, userId):
        message = self.messageRepository.getOnCooldownMessage(userId)

        if (message == None):
            return
        else:
            try:
                bot.delete_message(self.chatId, message.id)
                self.messageRepository.delete(message.id)
            except:
                self.messageRepository.delete(message.id)

    
    def DeleteHitAndCooldownMessages(self, userId):
        hitMessage = self.messageRepository.getHitMessage(userId)

        if(hitMessage == None):
            return
        else:
            bot.delete_message(self.chatId, hitMessage.id)
            self.messageRepository.delete(hitMessage.id)
        
        cooldownMessage = self.messageRepository.getCooldownMessage(userId)

        if (cooldownMessage == None):
            return
        else:
            bot.delete_message(self.chatId, cooldownMessage.id)
            self.messageRepository.delete(cooldownMessage.id)


    def DeleteMessage(self, messageId):
        message = self.messageRepository.get(messageId)
        if (message == None):
            return
        else:
            bot.delete_message(self.chatId, messageId)
            self.messageRepository.delete(messageId)
            return