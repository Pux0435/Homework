# Сделал Титов Максим 35 поток.
import telebot
from extensions import ConvertionException, CConvert

# Чтение token из файла
with open('tokenbot.txt', 'r') as file:
    TOKEN = file.read().strip()

bot = telebot.TeleBot(TOKEN)

keys = {'Биткоин': 'BTC', 'Доллар': 'USD', 'Лайткоин': 'LTC', 'Эфириум': 'ETH'} # Валюты можно добавлять и урезать

@bot.message_handler(commands=['start'])  # Приветственное сообщение
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет скиталец, {message.from_user.first_name},\nдабы понять. что и где жми /help")

@bot.message_handler(commands= ['help'])       # Инструкции
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n <имя валюты> \ <в какую валюту перевести> \ <количество переводимой валюты>\n /values <Список всех валют>'
    bot.reply_to(message, text)

@bot.message_handler(commands= ['values'])  # метод Показ валют
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types= ['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много\мало параметров')

        quote, base, amount = values
        total_base = CConvert.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)