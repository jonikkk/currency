from django import forms

from currency.models import Source, Rate, ContactUs


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('source_url', 'source_name', 'logo')


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('buy', 'sell', 'source', 'currency_type')


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = ('email_from', 'subject', 'message')
