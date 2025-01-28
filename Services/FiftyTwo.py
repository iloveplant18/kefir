import re

class FiftyTwo(object):
    def handle_message(self, message: str) -> str|None : 
        if (self.check_message(message)):
            return self.build_answer()
        return None
    
    def check_message(self, message: str) -> bool :
        if (re.match('^52|(п(и|ять|е)(д(и|е))?сят) два', message)):
            return True
        return False
    
    def build_answer(self, ) -> str:
        return '52 ха да ты юморист. Смешная цифра да?'