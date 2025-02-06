from config.bot_init import bot

class CharacterLogger(object):

    characterCard = "🦸‍♂️ **Игрок: {name}**\n" \
                    "📊 Уровень:  {level} ({exp} / {expNeed})\n\n" \
                    "Характеристики:\n" \
                    "❤️ Здоровье: {hp} HP\n" \
                    "⚔️ Физ. урон ближний: {minMeleeDmg} - {maxMeleeDmg}\n" \
                    "🏹 Физ. урон дальний: {minRangeDmg} - {maxRangeDmg}\n" \
                    "🔮 Маг. урон дальний: {minMagicDmg} - {maxMagicDmg}\n" \
                    "🌱 Сила лечения: {healPower}\n\n" \
                    "🛡️ Броня: {armor}\n" \
                    "💫 Маг. сопротивление: {elementalResistance}\n" \
    
    def __init__(self, chatId):
        self.chatId = chatId

    def logStats(self, characterInfoDto):
        response = self.characterCard.format(name=characterInfoDto.name,
                                        level=characterInfoDto.level,
                                        exp=characterInfoDto.exp,
                                        expNeed=characterInfoDto.expNeed,
                                        hp=characterInfoDto.hp,
                                        minMeleeDmg=characterInfoDto.minMeleeDmg,
                                        maxMeleeDmg=characterInfoDto.maxMeleeDmg,
                                        minRangeDmg=characterInfoDto.minRangeDmg,
                                        maxRangeDmg=characterInfoDto.maxRangeDmg,
                                        minMagicDmg=characterInfoDto.minMagicDmg,
                                        maxMagicDmg=characterInfoDto.maxMagicDmg,
                                        healPower=characterInfoDto.healPower,
                                        armor=characterInfoDto.armor,
                                        elementalResistance=characterInfoDto.elementalResistance,)
        
        return bot.send_message(self.chatId, response, parse_mode="Markdown").id

    def logCreation(self, userName):
        message =  f"{userName}, твой персонаж создан.\n" \
                    "Смотреть статы: /char\n" \
                    "Смортреть шмот: /inv"
        bot.send_message(self.chatId, message)

    def LogLevelUp(self, userName):
        message =  f"{userName}, ты повысил уровень\n"
        bot.send_message(self.chatId, message)