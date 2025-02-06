from Models.Character import Character

characters = dict()

#По хорошему репозиторий должен получать модель и мапить результаты в хранилище самостоятельно
class CharacterRepository(object):

    def get(self, userId: int) -> Character or None:
        if (self.checkIsCharacterExists(userId)):
            return characters[userId]

    def create(self, userId: int, name: str) -> Character or None:
        if (self.checkIsCharacterExists(userId)):
            return
        character = Character(userId, name)
        characters[userId] = character
        return character
    
    def update(self, characterId: int, newValues: dict):
        character = self.get(characterId)
        propertiesToUpdate = newValues.keys()
        for property in propertiesToUpdate:
            if hasattr(character, property):
                setattr(character, property, newValues[property])
            else:
                raise Exception('trying to update non existend property on character')

    def checkIsCharacterExists(self, userId) -> bool :
        if (userId in characters):
            return True
        return False