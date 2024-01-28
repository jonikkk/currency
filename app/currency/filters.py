import django_filters

from currency.models import Rate, Source, ContactUs


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = ['currency_type', 'buy', 'sell', 'created', 'source']


class SourceFilter(django_filters.FilterSet):
    class Meta:
        model = Source
        fields = ['source_name']


class ContactUsFilter(django_filters.FilterSet):
    class Meta:
        model = ContactUs
        fields = ['email_from', 'subject']
