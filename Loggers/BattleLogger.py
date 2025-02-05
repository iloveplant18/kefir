from config.bot_init import bot
from Services.Shared.OperationsService import OperationsService
from Loggers.BossLogger import BossLogger

class BattleLogger(object):

    hitPhrases = [
        '👊 {name} въебал на {damage} урона',
        '👊 {name}: Тычка {damage} урона'
    ]

    def __init__(self, chatId):
            self.chatId = chatId
            self.messageIdLast = None
            self.users_idToCooldownMessage = dict()
            self.users_idHitMessage = dict()

    def LogHit(self, userDto, damage):
        phrase = OperationsService.GetShuffledAnswer(self.hitPhrases)
        response = phrase.format(damage=damage, name=userDto.name)
        message = bot.send_message(self.chatId, response)
        self.users_idHitMessage[userDto.id] = message.id

    def RefreshEnemyInfo(self, messageId, bossInfoDto):
        response = BossLogger.bossCard.format(name=bossInfoDto.name,
                                    level=bossInfoDto.level,
                                    hp=bossInfoDto.hp,
                                    maxhp=bossInfoDto.maxhp,
                                    rarity=bossInfoDto.rarity)
        
        bot.edit_message_text(chat_id=self.chatId, message_id=messageId, text=response, parse_mode="Markdown")

    def LogOnCooldown(self, userName):
        phrase = f"{userName}, ты кд" #добавить сколько времени осталось
        self.messageIdLast = bot.send_message(self.chatId, phrase).id #TODO Баг: Почему то self.messageIdLast не обновляется
        return
    
    def LogToCooldown(self, userDto, cooldown):
        phrase = f'⌛ {userDto.name} в кд {cooldown} секунд'
        message = bot.send_message(self.chatId, phrase)
        self.users_idToCooldownMessage[userDto.id] = message.id

    def CleanLastCooldownLog(self):
        if(self.messageIdLast is not None):
            bot.delete_message(self.chatId, self.messageIdLast)
            return
        return
    
    def CleanToCooldownLog(self, userId):
        bot.delete_message(self.chatId, self.users_idToCooldownMessage[userId])
        del self.users_idToCooldownMessage[userId]
        return
    
    def CleanHitLog(self, userId):
        bot.delete_message(self.chatId, self.users_idHitMessage[userId])
        del self.users_idHitMessage[userId]
        return

    