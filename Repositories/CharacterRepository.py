from Models.Character import Character

characters = dict()

class CharacterRepository:

    def get(self, userId: int) -> Character or None:
        if (self.checkIsCharacterExists(userId)):
            return characters[userId]

    def create(self, userId: int, name: str, maxHp: int) -> Character or None:
        if (self.checkIsCharacterExists(userId)):
            return
        character = Character(userId, name, maxHp)
        characters[userId] = character
        return character

    def checkIsCharacterExists(self, userId) -> bool :
        if (userId in characters):
            return True
        return False