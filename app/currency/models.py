from django.db import models
from currency.choices import CurrencyTypeChoices


class Rate(models.Model):

    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sell = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    currency_type = models.SmallIntegerField(choices=CurrencyTypeChoices.choices, default=CurrencyTypeChoices.USD)
    source = models.CharField(max_length=255)


class ContactUs(models.Model):
    contact_id = models.AutoField(primary_key=True)
    email_from = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=2048)


class Source(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_url = models.CharField(max_length=255, blank=False)
    source_name = models.CharField(max_length=64, blank=False)
