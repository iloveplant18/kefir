import random

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
    
    @staticmethod
    def CheckLuck(chance) -> str:
        randomNumber = random.randint(1, 100)
        
        if (randomNumber <= chance):
            return True
        else:
            return False