from config.bot_init import bot
from Services.Shared.OperationsService import OperationsService
from Loggers.BossLogger import BossLogger

class BattleLogger(object):

    hitPhrases = [
        'Въебал на {damage} урона',
        'Тычка {damage} урона'
    ]

    def __init__(self, chatId):
            self.chatId = chatId
            self.messageIdLast = None

    def LogHit(self, userName, damage):
        phrase = OperationsService.GetShuffledAnswer(self.hitPhrases)
        response = phrase.format(damage=damage)
        bot.send_message(self.chatId, f"{userName}: {response}")

    def RefreshEnemyInfo(self, messageId, bossInfoDto):
         response = BossLogger.bossCard.format(name=bossInfoDto.name,
                                        level=bossInfoDto.level,
                                        hp=bossInfoDto.hp,
                                        maxhp=bossInfoDto.maxhp,
                                        rarity=bossInfoDto.rarity)
         
         bot.edit_message_text(chat_id=self.chatId, message_id=messageId, text=response)

    def LogOnCooldown(self, userName):
        phrase = f"{userName}, ты кд" #добавить сколько времени осталось
        self.messageIdLast = bot.send_message(self.chatId, phrase).id #TODO Баг: Почему то self.messageIdLast не обновляется
        return
    
    def LogToCooldown(self, userName, cooldown):
        phrase = f'{userName} в кд {cooldown} секунд'
        bot.send_message(self.chatId, phrase)

    def CleanLastCooldownLog(self):
        if(self.messageIdLast is not None):
            bot.delete_message(self.chatId, self.messageIdLast)
            return
        return

    