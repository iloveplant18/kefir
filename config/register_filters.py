from Filters.DepressionFilter import DepressionFilter
from Filters.HasCharacter import HasCharacter
from config.bot_init import bot

bot.add_custom_filter(DepressionFilter())
bot.add_custom_filter(HasCharacter())