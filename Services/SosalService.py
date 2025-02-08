from Services.Shared import OperationsService
from Services.Shared.OperationsService import OperationsService
from Services.Shared.Data import data
from config.bot_init import bot
import time

class SosalService(object):
    def Handle(self, chatId) -> str|None :

        responses = data["yesQuestions"]
        response = OperationsService.GetShuffledAnswer(responses)

        bot.send_message(chatId, response)

        time.sleep(2)

        bot.send_message(chatId, "Сосал?")