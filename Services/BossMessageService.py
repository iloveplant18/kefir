from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from Services.Shared.OperationsService import OperationsService
from Models.Message import Message
from config.bot_init import bot, inject

class BossMessageService(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, chatId):
        self.chatId = chatId
        self.messageRepository = inject._messageRepository
    
    spawnPhrases = [
        'Босс заспавнен',
        'Я вызвал босса, чуваки'
    ]

    killPhrases = [
        'Чмошный развалился, лут в след обновлениях (сосите)',
        'Ну вы крутые, мужики, он всё. лут в след обновлениях (сосите)'
    ]

    bossCard =  "🐉 **Босс: {name}**\n" \
                "❤️ HP: {hp} / {maxhp}\n\n" \
                "📊 Уровень:  {level}\n" \
                "💎 Редкость: {rarity}"
    
    battleReport =  " 🛠️ В разработке\n\n" \
                    "📝 **Отчет о бое**\n" \
                    "🐉 Босс: {name}\n\n" \
                    "💥 Урон:\n"

    def logSpawn(self):
        response = OperationsService.GetShuffledAnswer(self.spawnPhrases)
        bot.send_message(self.chatId, response)

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        hit_button = KeyboardButton("⚔ Ударить")
        markup.add(hit_button)
        messageId = bot.send_message(self.chatId, "Меню атак получено", reply_markup=markup).id

        message = Message(messageId, None)
        self.messageRepository.create(message)


    def SendBossCard(self, bossInfoDto):
        response = self.bossCard.format(name=bossInfoDto.name,
                                        level=bossInfoDto.level,
                                        hp=bossInfoDto.hp,
                                        maxhp=bossInfoDto.maxhp,
                                        rarity=bossInfoDto.rarity)
        
        messageId = bot.send_message(self.chatId, response, parse_mode="Markdown").id
        bot.pin_chat_message(self.chatId, message_id=messageId)

        message = Message(messageId, response, isBossCard=True)
        self.messageRepository.create(message)


    def LogKill(self, bossName, UsersDamageDto):
        responseKill = OperationsService.GetShuffledAnswer(self.killPhrases)
        responseReport = self.battleReport.format(name=bossName)
        for user in UsersDamageDto:
            line = f"{user.userName}: {user.hitpoints}\n"
            responseReport += line
        responseReport += "\nОпыт получают все, кто участвовал"

        messageId = bot.send_message(self.chatId, responseKill, reply_markup=ReplyKeyboardRemove()).id
        bot.send_message(self.chatId, responseReport, parse_mode="Markdown")

        message = Message(messageId, None)
        self.messageRepository.create(message)


    def RemoveBossCard(self):
        message = self.messageRepository.getBossCard()
        if (message == None):
            return
        else:
            bot.delete_message(self.chatId, message.id)
            self.messageRepository.delete(message.id)
            return