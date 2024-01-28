import random

from django.core.management import BaseCommand

from currency.choices import CurrencyTypeChoices
from currency.models import Rate, Source


class Command(BaseCommand):
    about = 'Generate 500 random currency rates'

    def handle(self, *args, **options):
        source, _ = Source.objects.get_or_create(
            code_name='dummy',
            defaults={
                'source_name': 'dummy',
                'source_url': 'https://dummy.com'
            })

        for _ in range(500):
            Rate.objects.create(
                buy=random.randint(30, 40),
                sell=random.randint(30, 40),
                currency_type=random.choice(CurrencyTypeChoices.choices)[0],
                source=source
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated 500 random currency rates'))
