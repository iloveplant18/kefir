from telebot.custom_filters import SimpleCustomFilter

from Repositories.CharacterRepository import CharacterRepository


class HasCharacter(SimpleCustomFilter):
    key = 'has_character'

    @staticmethod
    def check(message) -> bool:
        characterRepository = CharacterRepository()
        isUserHasCharacter = characterRepository.checkIsCharacterExists(message.from_user.id)
        if (isUserHasCharacter):
            return True
        return False