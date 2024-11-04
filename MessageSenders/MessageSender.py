from index import bot
from typing import List  

from Services import MessageSenderInterface 

class MessageSender(MessageSenderInterface):
    def send_all(self, chat_id, list_of_messages: List[str]) -> None :
        for i in list_of_messages:
            if (i['type'] == 'text'):
                self.send_text(chat_id, i['message'])
            elif (i['type'] == 'sticker'):
                self.send_sticker(chat_id, i['message'])

    def send_text(chat_id, message: str) -> None:
        bot.send_message(chat_id, message)
    
    def send_sticker(chat_id, sticker_name: str) -> None:
        bot.send_sticker(chat_id, sticker_name)
