from django.db import models
from currency.choices import CurrencyTypeChoices
from django.utils.translation import gettext_lazy as _


class Rate(models.Model):
    buy = models.DecimalField(_('Buy'), max_digits=10, decimal_places=2)
    sell = models.DecimalField(_('Sell'), max_digits=10, decimal_places=2)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    currency_type = models.SmallIntegerField(
        _('Currency type'),
        choices=CurrencyTypeChoices.choices,
        default=CurrencyTypeChoices.USD
    )
    source = models.CharField(_('Source'), max_length=255)

    class Meta:
        verbose_name = _('Rate')
        verbose_name_plural = _('Rates')


class ContactUs(models.Model):
    contact_id = models.AutoField(primary_key=True)
    email_from = models.EmailField(_('Email from'), )
    subject = models.CharField(_('Subject'), max_length=255)
    message = models.TextField(_('Message'), max_length=2048)

    class Meta:
        verbose_name = _('Contact Us')
        verbose_name_plural = _('Contact Us')


class Source(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_url = models.CharField(_('Source URL'), max_length=255, blank=False)
    source_name = models.CharField(_('Source name'), max_length=64, blank=False)

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')
