import telebot
from dotenv import load_dotenv
import os
from config.Inject import Inject

load_dotenv()

bot_key = os.getenv('BOT_KEY')
bot = telebot.TeleBot(bot_key)
inject = Inject()
