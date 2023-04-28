import requests

from db import new_currency, check_currency


def get_currency():
    USD = 840
    EUR = 978
    r = requests.get(url='https://api.monobank.ua/bank/currency')
    if r.status_code == 200:
        res = r.json()
        data = {}
        for i in res:
            if i['currencyCodeA'] == USD:
                buy_usd = i['rateBuy']
                sell_usd = i['rateSell']
                data['USD'] = [buy_usd, sell_usd]
            elif i['currencyCodeA'] == EUR and i['currencyCodeB'] == 980:

                buy_eur = i['rateBuy']
                sell_eur = i['rateSell']
                data['EUR'] = [buy_eur, sell_eur]
        res = new_currency(data)
        return data
    else:
        data = check_currency()
        return data

