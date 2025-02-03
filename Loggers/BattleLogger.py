from config.bot_init import bot
from Services.Shared.OperationsService import OperationsService

class BattleLogger(object):

    hitPhrases = [
        'Въебал на {damage} урона.\nУ лоха осталось {bossHp} хп',
        'Тычка {damage} урона, осталось {bossHp} хп'
    ]

    def __init__(self, chatId):
            self.chatId = chatId
            self.messageIdLast = None

    def LogHit(self, userName, damage, bossHp):
        phrase = OperationsService.GetShuffledAnswer(self.hitPhrases)
        response = phrase.format(damage=damage, bossHp=bossHp)
        bot.send_message(self.chatId, f"{userName}: {response}")

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

    