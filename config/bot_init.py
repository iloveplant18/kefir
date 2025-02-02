import telebot
from dotenv import load_dotenv
import os

load_dotenv()

bot_key = os.getenv('BOT_KEY')
bot = telebot.TeleBot(bot_key)