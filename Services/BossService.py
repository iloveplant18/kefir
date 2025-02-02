from Services.Shared.OperationsService import OperationsService
from telebot.types import ReplyKeyboardRemove
import time

class BossService(object):

    usersOnCooldown = set()
    isBossAlive = True

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

        # сейчас здесь случается некритичный баг, он должен  
        # пофикситься после создания класса атакующего
        if (userId in self.usersOnCooldown):
            self.bot.send_message(userId, "Ты кд")

        hpAfterHit = self.boss.GetHit(damage)
        
        if (hpAfterHit <= 0):
            hpAfterHit = 0
            self.isBossAlive = False
        
        BattleLogs.LogHit(self.chatId, self.bot, userName, damage, hpAfterHit)

        self.GoToCooldown(userId)
    

    def KillBoss(self):
        BattleLogs.LogKill(self.chatId, self.bot)

    # Нужны экз классов для каждого пользователя
    def SendBattleMarkups(self):
        for user in self.users:
            self.bot.send_message(user, "Меню атак получено", reply_markup=self.markup)

    def OutOfCooldown(self, user):
        cooldown = 30
        time.sleep(cooldown)
        self.usersOnCooldown.remove(user)
        self.bot.send_message(user, "Воюй дальше", reply_markup=self.markup)

    def GoToCooldown(self, user):
        self.usersOnCooldown.add(user)
        self.bot.send_message(user, 'В кд 30 секунд', reply_markup=ReplyKeyboardRemove())


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