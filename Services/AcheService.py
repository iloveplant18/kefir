from Services.Shared.OperationsService import OperationsService
from Services.SosalService import SosalService
from Services.Shared.Data import data
from config.bot_init import bot

class AcheService(object):
    def Handle(self, message: str) -> str|None :

        responses = ['аниче нах', 'аниче епта', 'хуй - вот те че', 'вова момент']

        request = 'аче'
        isTargetMessage = OperationsService.CheckInput(message, request)
        response = OperationsService.GetShuffledAnswer(responses)

        if (isTargetMessage):
            return response
        else:
            return None
        
class IcheService(object):
    def Handle(self, message: str) -> str|None :

        responses = ['иниче', 'похуй плюс похуй', 'ну похуй и похуй']

        request = 'иче'
        isTargetMessage = OperationsService.CheckInput(message, request)
        response = OperationsService.GetShuffledAnswer(responses)

        if (isTargetMessage):
            return response
        else:
            return None

# Случайная фраза прокает с определенным шансом на каждое сообщение
class RandomUntilConversationService(object):
    def Handle(self, chatId) -> str|None :

        chanceToLucky = 2
        isLucky = OperationsService.CheckLuck(chanceToLucky)

        if (isLucky):
            SosalService().Handle(chatId)
            return

        chanceToLucky = 8 #в целочисленных процентах от 1 до 100
        isLucky = OperationsService.CheckLuck(chanceToLucky)

        if (isLucky):
            responses = data["badPhrases"] + data["goodPhrases"]
            response = OperationsService.GetShuffledAnswer(responses)
            bot.send_message(chatId, response)
            return