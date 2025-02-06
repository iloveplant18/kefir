import uuid

class AttackDto:
    def __init__(self, damageDto, userDto, dateTime):
        self.id = uuid.uuid1
        self.damageDto = damageDto
        self.userDto = userDto
        self.dateTime = dateTime