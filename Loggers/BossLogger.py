from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from Services.BossService import BossService
from Services.Shared.OperationsService import OperationsService
from config.bot_init import bot


class BossLogger(object):

    spawnPhrases = [
        'Босс заспавнен',
        'Я вызвал босса, чуваки'
    ]

    killPhrases = [
        'Чмошный развалился, лут в след обновлениях (сосите)',
        'Ну вы крутые, мужики, он всё. лут в след обновлениях (сосите)'
    ]

    bossCard =  "🐉 Босс: {name}\n" \
                "❤️ Здоровье: {hp} HP / {maxhp} HP\n\n" \
                "📊 Уровень:  {level}\n" \
                "💎 Редкость: {rarity}"

    def __init__(self, chatId):
        self.chatId = chatId

    def logSpawn(self):
        response = OperationsService.GetShuffledAnswer(self.spawnPhrases)
        bot.send_message(self.chatId, response)

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        hit_button = KeyboardButton("⚔ Ударить")
        markup.add(hit_button)

    def SendBossCard(self, bossInfoDto):
        response = self.bossCard.format(name=bossInfoDto.name,
                                        level=bossInfoDto.level,
                                        hp=bossInfoDto.hp,
                                        maxhp=bossInfoDto.maxhp,
                                        rarity=bossInfoDto.rarity)
        
        return bot.send_message(self.chatId, response).id

    def LogKill(self):
        response = OperationsService.GetShuffledAnswer(self.killPhrases)
        bot.send_message(self.chatId, response, reply_markup=ReplyKeyboardRemove())