from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message
import re

class DepressionFilter(SimpleCustomFilter):
    key = 'depression_filter'

    @staticmethod
    def check(message: Message) -> bool:
        if re.match("у м[еи]ня д[еи]пресс?(ия|я|ея)", message.text):
            return True
        return False
