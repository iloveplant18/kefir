from Services.Shared.OperationsService import OperationsService
from telebot.types import ReplyKeyboardRemove
from datetime import datetime, time

class BossService(object):

    usersOnCooldown = dict()
    isBossAlive = True
    messageIdCooldownLast = None

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
        
        if (self.CheckCooldown(userId) == True):
            if(self.CheckReload(userId, userName, cooldownSeconds=30) == True):
                self.OutOfCooldown(userId, userName)

        if (self.CheckCooldown(userId) == True):
            messageIdCooldown = BattleLogs.LogOnCooldown(self.chatId, self.bot, userName)
            BattleLogs.LogCleanLastCooldown(self.chatId, self.bot, self.messageIdCooldownLast)
            self.messageIdCooldownLast = messageIdCooldown
            return
        else:
            hpAfterHit = self.boss.GetHit(damage)
            
            if (hpAfterHit <= 0):
                hpAfterHit = 0
                self.isBossAlive = False

            BattleLogs.LogHit(self.chatId, self.bot, userName, damage, hpAfterHit)

            self.GoToCooldown(userId, userName)
            BattleLogs.LogToCooldown(self.chatId, self.bot, userName, cooldown=30)

            return
    
    def CheckCooldown(self, userId):
        usersOnCooldown = list(self.usersOnCooldown.keys())
        if (str(userId) in usersOnCooldown):
            return True
        else:
            return False

    def CheckReload(self, userId, userName, cooldownSeconds):

        timeDeltaCooldown = Calculations.getCooldownTimeDelta(cooldownSeconds)

        dateTimeNow = Calculations.getNowDateTime()
        dateTimeAttack = self.usersOnCooldown[f"{userId}"]

        timeDeltaLeft = dateTimeNow - dateTimeAttack

        if (timeDeltaLeft > timeDeltaCooldown):
            return True
        else:
            return False
    
    def KillBoss(self):
        BattleLogs.LogKill(self.chatId, self.bot)

    def SendBattleMarkups(self):
        self.bot.send_message(self.chatId, "Меню атак получено", reply_markup=self.markup)

    def OutOfCooldown(self, userId, userName):
        del self.usersOnCooldown[f"{userId}"]

    def GoToCooldown(self, userId, userName):
        dateTimeNow = Calculations.getNowDateTime()
        self.usersOnCooldown[f"{userId}"] = dateTimeNow
        

class Calculations(object):

    @staticmethod
    def parseTime(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        return hours, minutes, seconds
    
    @staticmethod
    def getNowDateTime():
        timeNow = datetime.now().time()
        return datetime.combine(datetime.min, timeNow)
    
    @staticmethod
    def getCooldownTimeDelta(seconds):
        cooldownTime = Calculations.parseTime(seconds)
        timeCooldown = time(hour=cooldownTime[0], minute=cooldownTime[1], second=cooldownTime[2])
        timeDeltaCooldown = datetime.combine(datetime.min, timeCooldown) - datetime.min
        return timeDeltaCooldown

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

    @staticmethod
    def LogOnCooldown(chatId, bot, userName):
        phrase = f"{userName}, ты кд" #добавить сколько времени осталось
        return bot.send_message(chatId, phrase).id
    
    @staticmethod
    def LogToCooldown(chatId, bot, userName, cooldown):
        phrase = f'{userName} в кд {cooldown} секунд'
        bot.send_message(chatId, phrase)

    @staticmethod
    def LogCleanLastCooldown(chatId, bot, messageIdLast):
        if(messageIdLast is not None):
            bot.delete_message(chatId, messageIdLast)