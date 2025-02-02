from Models.Character import Character


class CharacterService:

    def __init__(self, characterRepository, logger):
        self.characterRepository = characterRepository
        self.logger = logger

    def showCharacter(self, character: Character):
        self.logger.logStats(character)

    def createCharacter(self, userId: int, name: str, maxHp: int) -> Character or None:
        character = self.characterRepository.create(userId, name, maxHp)
        self.logger.logCreation(character)
