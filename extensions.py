import requests
import json

keys = {'Биткоин': 'BTC', 'Доллар': 'USD', 'Лайткоин': 'LTC', 'Эфириум': 'ETH'} # Валюты можно добавлять и урезать
class ConvertionException(Exception):
    pass

class CConvert:   # Ошибочки
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Невозможно конвертировать одну и ту же {base}.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось конвертировать валюту {quote}.')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось конвертировать валюту {base}.')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

# Api сервака можно изменить на свой другой
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        data = json.loads(r.content)
        if base_ticker not in data:
            raise ConvertionException(f'Не удалось получить данные для конвертации из {quote} в {base}')

        exchange_rate = data[base_ticker]   # Расчёт количества
        total_base = round(amount * exchange_rate, 2)
        return total_base