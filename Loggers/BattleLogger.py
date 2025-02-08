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

    def LogHit(self, userDto, damage):
        phrase = OperationsService.GetShuffledAnswer(self.hitPhrases)
        response = phrase.format(damage=damage, name=userDto.name)
        messageId = bot.send_message(self.chatId, response).id
        return messageId

    def RefreshEnemyInfo(self, messageId, bossInfoDto):
        response = BossLogger.bossCard.format(name=bossInfoDto.name,
                                    level=bossInfoDto.level,
                                    hp=bossInfoDto.hp,
                                    maxhp=bossInfoDto.maxhp,
                                    rarity=bossInfoDto.rarity)
        
        bot.edit_message_text(chat_id=self.chatId, message_id=messageId, text=response, parse_mode="Markdown")

    def LogOnCooldown(self, userName):
        phrase = f"{userName}, ты кд" #добавить сколько времени осталось
        messageId = bot.send_message(self.chatId, phrase).id #TODO Баг: Почему то self.messageIdLast не обновляется
        return messageId
    
    def LogToCooldown(self, userDto, cooldown):
        phrase = f'⌛ {userDto.name} в кд {cooldown} секунд'
        messageId = bot.send_message(self.chatId, phrase).id
        return messageId

    