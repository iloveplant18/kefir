#Можно сделать репозитории и сущности под каждый тип сообщений, но мне впадлу
class Message(object):
    
    def __init__(self,
                 id,
                 text,
                 isCooldownMessage = False,
                 isOnCooldownMessage = False,
                 isHitMessage = False,
                 isBossCard = False,
                 userId = None):
        self.id = id
        self.text = text
        self.isCooldownMessage = isCooldownMessage
        self.isOnCooldownMessage = isOnCooldownMessage
        self.isHitMessage = isHitMessage
        self.isBossCard = isBossCard
        self.userId = userId