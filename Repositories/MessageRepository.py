from Models.Message import Message

class MessageRepository:
        
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    messages = list()

    def get(self, messageId: int) -> Message or None:
        return next((m for m in self.messages if m.id == messageId), None)
    
    def getAll(self):
        return self.messages
    
    def getBossCard(self):
        return next((m for m in self.messages if m.isBossCard == True), None)
    
    def getOnCooldownMessage(self, userId: int):
        return next((m for m in self.messages if m.isOnCooldownMessage == True and m.userId == userId), None)
    
    def getHitMessage(self, userId):
        return next((m for m in self.messages if m.isHitMessage == True and m.userId == userId), None)
    
    def getCooldownMessage(self, userId):
        return next((m for m in self.messages if m.isCooldownMessage == True and m.userId == userId), None)

    def create(self, model) -> str or None:

        if (next((m for m in self.messages if m.id == model.id), None) is not None):
            return
        
        self.messages.append(model)

        return model.id
    
    def update(self, messageId: int, newValues: dict):

        message = self.get(messageId)
        propertiesToUpdate = newValues.keys()

        for property in propertiesToUpdate:
            if hasattr(message, property):
                setattr(message, property, newValues[property])
            else:
                raise Exception('trying to update non existend property on character')
            
    def delete(self, messageId) -> True :
        message = self.get(messageId)
        if(message is not None):
            self.messages.remove(message)
        return True