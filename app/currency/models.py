from django.db import models
from currency.choices import CurrencyTypeChoices
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static


def source_directory_path(instance, filename):
    return f'logo/source_{instance.source_name}/{filename}'


class Rate(models.Model):
    buy = models.DecimalField(_('Buy'), max_digits=10, decimal_places=2)
    sell = models.DecimalField(_('Sell'), max_digits=10, decimal_places=2)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    currency_type = models.SmallIntegerField(
        _('Currency type'),
        choices=CurrencyTypeChoices.choices,
        default=CurrencyTypeChoices.USD
    )
    source = models.ForeignKey('currency.Source', on_delete=models.CASCADE, related_name='rates')

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
    code_name = models.CharField(_('Code name'), max_length=64, unique=True)
    source_url = models.CharField(_('Source URL'), max_length=255, blank=False)
    source_name = models.CharField(_('Source name'), max_length=64, blank=False)
    logo = models.FileField(_('Logo'), default=None, null=True, blank=True, upload_to=source_directory_path)

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')

    def __str__(self):
        return self.source_name

    @property
    def logo_url(self) -> str:
        if self.logo:
            return self.logo.url

        return static('bank.png')


class RequestResponseTimeMiddlewareModel(models.Model):
    path = models.CharField(max_length=255)
    request_method = models.CharField(max_length=20)
    execute_time = models.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        verbose_name = _('Log')
        verbose_name_plural = _('Logs')
