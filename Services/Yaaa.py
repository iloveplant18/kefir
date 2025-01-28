
import re

class Yaaa(object):
    def handle_message(self, message: str) -> str|None :
        if (self.check_message(message)):
            return self.build_answer(message)
        return None
    
    def check_message(seld, message: str) -> bool :
        if (re.match('^я{3,}$', message)):
            return True
        return False
    
    def build_answer(self, message) -> str:
        return 'нет ' + message