from Models.Character import Character

#По хорошему репозиторий должен получать модель и мапить результаты в хранилище самостоятельно
class CharacterRepository(object):
    
    _instance = None
    characters = list()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get(self, userId: int) -> Character or None:
        print("Чтение", self.characters)
        return next((c for c in self.characters if c.userId == userId), None)

    def create(self, model) -> str or None:

        if (next((c for c in self.characters if c.userId == model.userId), None) is not None):
            return
        
        self.characters.append(model)

        print("Создание", self.characters)

        return model.userId
    
    def update(self, userId: int, newValues: dict):
        character = self.get(userId)
        propertiesToUpdate = newValues.keys()
        for property in propertiesToUpdate:
            if hasattr(character, property):
                setattr(character, property, newValues[property])
            else:
                raise Exception('trying to update non existend property on character')