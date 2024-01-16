from time import sleep

from bs4 import BeautifulSoup
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import requests

from currency.choices import CurrencyTypeChoices
from currency.constants import PRIVATBANK_CODE_NAME, MONOBANK_CODE_NAME, OBMEN_DP_UA_CODE_NAME, UAH_CODE
from currency.models import Rate, Source
from currency.utils import to_2_places_decimal


@shared_task
def parse_privatbank():
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()

    source, _ = Source.objects.get_or_create(
        code_name=PRIVATBANK_CODE_NAME,
        defaults={
            'source_name': 'PrivatBank',
            'source_url': url
        })

    available_currency_types = {
        'USD': CurrencyTypeChoices.USD,
        'EUR': CurrencyTypeChoices.EUR,
    }

    for rate in rates:
        buy = to_2_places_decimal(rate['buy'])
        sell = to_2_places_decimal(rate['sale'])
        currency_type = rate['ccy']

        if currency_type not in available_currency_types:
            continue

        currency_type = available_currency_types[currency_type]

        last_rate = Rate.objects.filter(currency_type=currency_type, source=source).order_by('-created').first()

        if last_rate is None or last_rate.buy != buy or last_rate.sell != sell:
            Rate.objects.create(
                buy=buy,
                sell=sell,
                currency_type=currency_type,
                source=source

            )


@shared_task()
def parse_monobank():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()

    source, _ = Source.objects.get_or_create(
        code_name=MONOBANK_CODE_NAME,
        defaults={
            'source_name': 'MonoBank',
            'source_url': url
        })

    available_currency_types = {
        840: CurrencyTypeChoices.USD,
        978: CurrencyTypeChoices.EUR,
    }

    for rate in rates:
        if 'rateCross' in rate:
            continue
        buy = to_2_places_decimal(rate['rateBuy'])
        sell = to_2_places_decimal(rate['rateSell'])
        currency_type = rate['currencyCodeA']

        if currency_type not in available_currency_types or rate['currencyCodeB'] != UAH_CODE:
            continue

        currency_type = available_currency_types[currency_type]

        last_rate = Rate.objects.filter(currency_type=currency_type, source=source).order_by('-created').first()

        if last_rate is None or last_rate.buy != buy or last_rate.sell != sell:
            Rate.objects.create(
                buy=buy,
                sell=sell,
                currency_type=currency_type,
                source=source

            )


@shared_task
def parse_website_obmen_dp_ua():
    url = 'https://obmen.dp.ua/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rates = {}

    parse_rates = soup.find('ul', class_="currencies__list").findAll('li', class_='currencies__block')
    for rate in parse_rates:
        currency_type = rate.find(
            'div', class_="currencies__block-link gtm-currency-pair"
        ).find('div', class_="currencies__block-name").text.replace('Курс', '')
        buy = rate.find(
            'div', class_="currencies__block-link gtm-currency-pair"
        ).find('div', class_="currencies__block-buy").text.replace('\xa0', '')
        sell = rate.find(
            'div', class_="currencies__block-link gtm-currency-pair"
        ).find('div', class_="currencies__block-sale").text.replace('\xa0', '')
        rates[currency_type] = {
            'buy': buy,
            'sell': sell
        }

    available_currency_types = {
        ' USD/UAH': CurrencyTypeChoices.USD,
        ' EUR/UAH': CurrencyTypeChoices.EUR,
    }

    for rate in rates:
        buy = to_2_places_decimal(rates[rate]['buy'])
        sell = to_2_places_decimal(rates[rate]['sell'])
        currency_type = rate

        if currency_type not in available_currency_types:
            continue

        currency_type = available_currency_types[currency_type]

        source, _ = Source.objects.get_or_create(
            code_name=OBMEN_DP_UA_CODE_NAME,
            defaults={
                'source_name': 'Obmen.dp.ua',
                'source_url': url
            })

        last_rate = Rate.objects.filter(currency_type=currency_type, source=source).order_by('-created').first()

        if last_rate is None or last_rate.buy != buy or last_rate.sell != sell:
            Rate.objects.create(
                buy=buy,
                sell=sell,
                currency_type=currency_type,
                source=source

            )


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5})
def send_email_in_background(subject, message, email_from):
    sleep(10)
    send_mail(
        subject,
        message,
        email_from,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
