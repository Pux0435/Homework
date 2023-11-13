import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

# Ваш токен для доступа к Telegram API
TELEGRAM_TOKEN = '6527803065:AAEczlWAVNpZE8j25JyEvA0KqL-iQpu_RJA'

# Ваш токен для доступа к WeatherAPI
WEATHERAPI_TOKEN = '5c4edea6d96f4c2b8db190643232008'

# Функция для получения погоды
def get_weather(city):
    base_url = f"http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHERAPI_TOKEN,
        "q": city,
        "aqi": "no"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data
def start(update, context):
    update.message.reply_text("Привет скиталец! Я погодный бот. Выберите город из списка кнопок или введите название города.", reply_markup=get_keyboard())

def get_weather_forecast(city):
    base_url = f"http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": WEATHERAPI_TOKEN,
        "q": city,
        "days": 5,  # Получение прогноза на 5 дней
        "aqi": "no"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

# Функция для создания клавиатуры с кнопками
def get_keyboard():
    keyboard = [
        ["Усолье-Сибирское", "Паттайя"],
        ["Введите город вручную"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Обработчик текстовых сообщений
def get_weather_info(update, context):
    if update.message.text == "Введите город вручную":
        update.message.reply_text("Введите название города.")
        return
    city = update.message.text
    weather_data = get_weather_forecast(city)

    if "error" not in weather_data:
        forecast_days = weather_data["forecast"]["forecastday"]
        message = f"Прогноз погоды в городе {city} на 5 дней:\n"
        for day in forecast_days:
            date = day["date"]
            max_temp = day["day"]["maxtemp_c"]
            min_temp = day["day"]["mintemp_c"]
            message += f"{date}:, Мин: {min_temp}°C, Макс: {max_temp}°C\n"
    else:
        message = "Извините, не удалось получить прогноз погоды."

    update.message.reply_text(message)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_weather_info))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()