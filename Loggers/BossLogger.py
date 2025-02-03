from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from Services.BossService import BossService
from Services.Shared.OperationsService import OperationsService
from config.bot_init import bot


class BossLogger(object):

    spawnPhrases = [
        'Босс заспавнен, у него {bossHp} здоровья',
        'Я вызвал босса, чуваки, у него {bossHp} здоровья'
    ]

    killPhrases = [
        'Чмошный развалился, лут в след обновлениях (сосите)',
        'Ну вы крутые, мужики, он всё. лут в след обновлениях (сосите)'
    ]

    def __init__(self, chatId):
        self.chatId = chatId

    def logSpawn(self, bossHp):
        phrase = OperationsService.GetShuffledAnswer(self.spawnPhrases)
        response = phrase.format(bossHp=bossHp)
        bot.send_message(self.chatId, response)

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        hit_button = KeyboardButton("⚔ Ударить")
        markup.add(hit_button)
        bot.send_message(self.chatId, "Меню атак получено", reply_markup=markup)

    def LogKill(self):
        response = OperationsService.GetShuffledAnswer(self.killPhrases)
        bot.send_message(self.chatId, response, reply_markup=ReplyKeyboardRemove())