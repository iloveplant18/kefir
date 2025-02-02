from Services.Shared.OperationsService import OperationsService
from telebot.types import ReplyKeyboardRemove
from datetime import datetime

class BossService(object):

    usersOnCooldown = dict()
    isBossAlive = True
    lastCDMessageId = None

    #Фразы позже переедут в другое место
    spawnPhrases = [
        'Босс заспавнен, у него {bossHp} здоровья', 
        'Я вызвал босса, чуваки, у него {bossHp} здоровья'
    ]

    hitPhrases = [
        'Въебал на {damage} урона.\nУ лоха осталось {bossHp} хп', 
        'Тычка {damage} урона, осталось {bossHp} хп'
    ]

    killPhrases = [
        'Чмошный развалился, лут в след обновлениях (сосите)', 
        'Ну вы крутые, мужики, он всё. лут в след обновлениях (сосите)'
    ]

    def __init__(self, chatId, bot, markup, users):
        self.chatId = chatId
        self.bot = bot
        self.markup = markup
        self.users = users

    def SpawnBoss(self, hp):
        self.boss = Boss(hp)
        BattleLogs.LogSpawn(self.chatId, self.bot, self.boss.hp)
        self.SendBattleMarkups()

    def HitBoss(self, message, damage):

        userId = message.from_user.id
        userName = message.from_user.first_name
        
        #порефакторить
        usersOnCooldown = list(self.usersOnCooldown.keys())
        if (str(userId) in usersOnCooldown):
            cooldown = datetime(2025, 2, 2, 0, 0, 30).time()
            cooldown = datetime.combine(datetime.min, cooldown)
        
            time = datetime.now().time()
            time = datetime.combine(datetime.min, time)

            timeLeft = time - self.usersOnCooldown[f"{userId}"]
            if (timeLeft > cooldown - datetime.min):
                self.OutOfCooldown(userId, userName)
            else:
                cDMessageId = self.bot.send_message(self.chatId, f'{userName}, ты кд')
                if(self.lastCDMessageId is not None):
                    self.bot.delete_message(self.chatId, self.lastCDMessageId)
                self.lastCDMessageId = cDMessageId.id
                return

        hpAfterHit = self.boss.GetHit(damage)
        
        if (hpAfterHit <= 0):
            hpAfterHit = 0
            self.isBossAlive = False
        
        BattleLogs.LogHit(self.chatId, self.bot, userName, damage, hpAfterHit)

        self.GoToCooldown(userId, userName)

        return

    def KillBoss(self):
        BattleLogs.LogKill(self.chatId, self.bot)

    def SendBattleMarkups(self):
        self.bot.send_message(self.chatId, "Меню атак получено", reply_markup=self.markup)

    def OutOfCooldown(self, userId, userName):
        del self.usersOnCooldown[f"{userId}"]

    def GoToCooldown(self, userId, userName):
        time = datetime.now().time()
        time = datetime.combine(datetime.min, time)
        self.usersOnCooldown[f"{userId}"] = time
        self.bot.send_message(self.chatId, f'{userName} в кд 30 секунд')


class Boss(object):

    def __init__(self, hp):
        self.hp = hp

    def GetHit(self, damage):
        self.hp -= damage
        return self.hp
    

class BattleLogs(object):

    @staticmethod
    def LogHit(chatId, bot, userName, damage, bossHp):
        phrase = OperationsService.GetShuffledAnswer(BossService.hitPhrases)
        response = phrase.format(damage=damage, bossHp=bossHp)
        bot.send_message(chatId, f"{userName}: {response}")

    @staticmethod
    def LogKill(chatId, bot):
        response = OperationsService.GetShuffledAnswer(BossService.killPhrases)
        bot.send_message(chatId, response, reply_markup=ReplyKeyboardRemove())

    @staticmethod
    def LogSpawn(chatId, bot, bossHp):
        phrase = OperationsService.GetShuffledAnswer(BossService.spawnPhrases)
        response = phrase.format(bossHp=bossHp)
        bot.send_message(chatId, response)