from rest_framework import serializers

from currency.models import Rate, ContactUs, Source
from currency.tasks import send_email_in_background


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'buy',
            'sell',
            'created',
            'currency_type',
            'source',

        )


class ContactUsSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        contact_us = ContactUs.objects.create(**validated_data)
        send_email_in_background.apply_async(
            kwargs={
                "subject": contact_us.subject,
                "message": contact_us.message,
                "email_from": contact_us.email_from
            },
            countdown=10,
        )
        return contact_us

    class Meta:
        model = ContactUs
        fields = (
            'contact_id',
            'email_from',
            'subject',
            'message',
        )


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'id',
            'source_name',
            'source_url',
        )
