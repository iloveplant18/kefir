from config.bot_init import bot


class CharacterLogger:
    def __init__(self, chatId):
        self.chatId = chatId

    def logStats(self, character):
        message = f"{character.name}, hp: {character.hp}/{character.maxHp}"
        bot.send_message(self.chatId, message)

    def logCreation(self, character):
        message = f"Создан персонаж: \nИмя: {character.name} \nhp: {character.hp}/{character.maxHp}"
        bot.send_message(self.chatId, message)