from config.bot_init import bot
from Services.AcheService import AcheService, IcheService, RandomUntilConversationService
from Services.BossService import BossService
import random
import threading
import config.register_filters
from telebot.types import BotCommand, ReplyKeyboardMarkup, KeyboardButton

bossService = None
bot.set_my_commands([
    BotCommand("battles", "В боевой режим"),
    BotCommand("chill", "В мирный режим"),
    BotCommand("boss", "Призвать босса"),
])

battleUsers = set()
bossService = None

@bot.message_handler(commands=['battles'])
def start(message):
    chatId = message.chat.id
    userId = message.from_user.id
    userName = message.from_user.first_name

    if (userId in battleUsers):
        bot.send_message(chatId, f"{userName}, дохуя агрессивный? ты уже в боевом режиме")
        return

    if (userId not in battleUsers and bossService is not None):
        bot.send_message(chatId, f"{userName}, ну и где ты был? Жди некст босса теперь")
        return

    battleUsers.add(userId)

    bot.send_message(chatId, f"{userName} вошел в боевой режим")
    return

@bot.message_handler(commands=['chill'])
def start(message):
    chatId = message.chat.id
    userId = message.from_user.id
    userName = message.from_user.first_name

    if (userId not in battleUsers):
        bot.send_message(chatId, f"{userName}, чилл, чиииллл")
        return
    
    if (userId in battleUsers and bossService is not None):
        bot.send_message(chatId, f"{userName}, сражайся, сучара ссыкливая")
        return

    battleUsers.remove(userId)

    bot.send_message(chatId, f"{userName} вышел из боевого режима")
    return
    
@bot.message_handler(commands=['boss'])
def start(message):
    global bossService
    userId = message.from_user.id

    bot.delete_message(message.chat.id, message.message_id)

    if (userId not in battleUsers):
        bot.send_message(message.chat.id, "Чтобы драться с боссом, нужно быть в режиме боя")
        return
    
    if (bossService is not None):
        bot.send_message(message.chat.id, "Вы че, добейте этого сначала")
        return
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        hit_button = KeyboardButton("⚔ Ударить")
        markup.add(hit_button)

        bossService = BossService(message.chat.id, bot, markup, battleUsers)
        bossService.SpawnBoss(random.randint(60, 80))
        return

@bot.message_handler(func=lambda message: message.text == "⚔ Ударить")
def start(message):
    global bossService
    chatId = message.chat.id
    userId = message.from_user.id

    bot.delete_message(chatId, message.message_id)

    if (bossService == None):
        bot.send_message(chatId, 'Челы, бить некого, чильтесь')
        return 
    
    bossService.HitBoss(message, random.randint(1, 8))

    if (bossService.isBossAlive == False):
        bossService.KillBoss()
        bossService = None
        return
    
    threading.Thread(target=bossService.OutOfCooldown(userId)).start()
    return

@bot.message_handler(depression_filter=True)
def depression_controller(message):
    bot.reply_to(message, 'заплачь')

@bot.message_handler()
def message_handler(message):
    service = AcheService()
    response = service.Handle(message.text)
    if response:
        bot.send_message(message.chat.id, response)
        return

    service = IcheService()
    response = service.Handle(message.text)
    if (response):
        bot.send_message(message.chat.id, response)
        return

    # Случайная фраза прокает с определенным шансом на каждое сообщение
    service = RandomUntilConversationService()
    response = service.Handle(message.text)
    if (response):
        bot.send_message(message.chat.id, response)
        return

# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, 'ПОГНАЛИ НАХУЙ ЙОБАНЫЙ В РОТ')

# @bot.message_handler(commands=['help'])
# def help(message):
#     bot.send_message(message.chat.id, 'Спасибо, мне не нужна ваша помощь')

# alcohol_otvetki = [
#     'мальчики не пейте писька отсохнет',
#     'кто пьет тот короче потом ваще сосет хаха',
#     'кто короче вот это вот бухает да тот не шарит ваще ауф',
#     'а алкоголь через задницу действует быстрее. кто повелся тот пидор',
#     '''Если куришь ты табак,
# Значит ты пока дурак!
# Если хочешь стать дебилом
# Отравись еще и пивом!''',
# '''Тот кто курит или пьёт -
# Тот Россию предаёт.
# А кто не курит и не пьет -
# Тот настоящий патриот.''',
# '''Две бутылки самогона,
# «Беломора» пачка.
# Никогда вас не забудет
# Белая горячка!''',
# '''Было "Три богатыря",
# Стало три калеки.
# Может, пиво пили зря
# Эти человеки?!''',
# '''от вина одна беда,
# от курения - горе.
# до чего страну довёл
# алкоголик боря!''',
# ] 

# @bot.message_handler(commands=['antialcohol_propaganda'])
# def start(message):
#     t = monotonic()
#     while True:
#         if monotonic() - t > 60:
#             t = monotonic()
#             send_random_message(alcohol_otvetki, message.chat.id)

# @bot.message_handler(commands=['joke'])
# def joke(message):
#     joke = json.loads(requests.get('https://v2.jokeapi.dev/joke/Any?type=single').text)['joke']
#     bot.send_message(message.chat.id, joke)

# @bot.message_handler()
# def messages_handler(message):
#     if (message.from_user.id == 808356158): 
#         randValue = random.random()
#         if (randValue > 0.95):
#             bot.delete_message(message.chat.id, message.id)
#             return

#     depression = Depression()
#     depressionAnswer = depression.handle_message(message.text)
#     if (depressionAnswer):
#         bot.send_message(message.chat.id, depressionAnswer)

#     fifty_two = FiftyTwo()
#     answer = fifty_two.handle_message(message.text)
#     if (answer):
#         bot.send_message(message.chat.id, answer)

#     yaaa = Yaaa()
#     answer = yaaa.handle_message(message.text)
#     if (answer):
#         bot.send_message(message.chat.id, answer)

#     if (re.search('(^|\w*)да$', message.text.lower())):
#         bot.send_message(message.chat.id, 'пизда')
#         return

#     if (re.search('(^|\w*)нет$', message.text.lower())):
#         bot.send_message(message.chat.id, 'пидора ответ')
#         return

#     otvetki = ['баланду не малявим фраерок', 'бро мат для слабых духомм', 'кто много ругается в того ракеты летят (с. Батюшка)', 
#     'мне хочется кричать вам зачем вы славите дьявола хуепуталы хватит ругаться', 'ха во ты выдал', 'не ругаемся девчата', 'жопа хе']
#     if (re.search('б(и|а)?ля(ть)?|сук|ху(й|я|и|е|ё)|пизд', message.text.lower())):
#         send_random_message(otvetki, message.chat.id)

#     if (re.match('имба', message.text.lower())):
#         bot.send_message(message.chat.id, 'ваще ахуй 12/10 по фаренгейту жопа оторвалась прям')

#     if (re.match('Kefir119Bot', message.text)):
#         bot.send_message(message.chat.id, 'хватит меня тегать я на работе', 'html', True, False, message.id)

#     if (re.search('ладно', message.text)):
#         bot.send_message(message.chat.id, 'прохладно')



# # @bot.message_handler(commands=['antialcoholpropaganda'])
# # def antialcohol_propaganda(message):      
  
# def send_random_message(array, chat_id):
#     index = math.floor(random.random() * len(array))
#     bot.send_message(chat_id, array[index]) 

bot.infinity_polling()  