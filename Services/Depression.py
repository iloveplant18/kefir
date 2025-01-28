
import re

class Depression(object):
    def handle_message(self, text: str) -> str|None :
        if (self.depression_check(text)):
            return self.build_answer()
        return None

    def depression_check(self, text: str) -> bool : 
        if re.match("у м(е|и)ня д(е|и)пресс?(ия|я|ея)", text):
            return True
        return False
    
    def build_answer(self) -> str :
        return 'заплачь'