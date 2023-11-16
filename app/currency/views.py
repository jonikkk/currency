from django.http import HttpResponse
from django.shortcuts import render

from currency.models import Rate, ContactUs


# Create your views here.


def rate_list(request):
    result = []
    rates = Rate.objects.all()
    for rate in rates:
        result.append(
            f" ID: {rate.id}, "
            f"Buy: {rate.buy}, "
            f"Sell: {rate.sell}, "
            f"Created: {rate.created}, "
            f"Type: {rate.type}, "
            f"Source: {rate.source} <br>")

    return HttpResponse(str(result))


def contactus(request):
    result = []
    contacts = ContactUs.objects.all()
    for contact in contacts:
        result.append(
            f" ID: {contact.id}, "
            f"Email: {contact.email_from}, "
            f"Subject: {contact.subject}, "
            f"Message: {contact.message} <br>")

    return HttpResponse(str(result))
