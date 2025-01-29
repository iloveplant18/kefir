import random

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
    
class OperationsService():

    @staticmethod
    def CheckInput(message: str, request: str) -> bool :
        if (message == request):
            return True
        else:
            return False
    
    @staticmethod
    def GetShuffledAnswer(response) -> str:
        answerNumber = random.randint(0, len(response) - 1)
        return response[answerNumber]