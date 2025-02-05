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

    bossCard =  "🐉 **Босс: {name}**\n" \
                "❤️ Здоровье: {hp} HP / {maxhp} HP\n\n" \
                "📊 Уровень:  {level}\n" \
                "💎 Редкость: {rarity}"
    
    battleReport =  " 🛠️ В разработке\n\n" \
                    "📝 **Отчет о бое**\n" \
                    "🐉 Босс: {name}\n\n" \
                    "💥 Урон:\n" \
                    "[Игрок1]: [урон]\n" \
                    "[Игрок2]: [урон]\n" \
                    "...\n" \
                    "Лут..." \

    def __init__(self, chatId):
        self.chatId = chatId

    def logSpawn(self):
        response = OperationsService.GetShuffledAnswer(self.spawnPhrases)
        bot.send_message(self.chatId, response)

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        hit_button = KeyboardButton("⚔ Ударить")
        markup.add(hit_button)
        bot.send_message(self.chatId, "Меню атак получено", reply_markup=markup)

    def SendBossCard(self, bossInfoDto):
        response = self.bossCard.format(name=bossInfoDto.name,
                                        level=bossInfoDto.level,
                                        hp=bossInfoDto.hp,
                                        maxhp=bossInfoDto.maxhp,
                                        rarity=bossInfoDto.rarity)
        
        return bot.send_message(self.chatId, response, parse_mode="Markdown").id

    def LogKill(self, bossInfoDto):
        responseKill = OperationsService.GetShuffledAnswer(self.killPhrases)
        responseReport = self.battleReport.format(name=bossInfoDto.name)

        bot.send_message(self.chatId, responseKill, reply_markup=ReplyKeyboardRemove())
        bot.send_message(self.chatId, responseReport, parse_mode="Markdown")

    def RemoveBossCard(self, messageId):
        bot.delete_message(self.chatId, messageId)
        return