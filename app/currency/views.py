from django.shortcuts import render

from currency.models import Rate, ContactUs


# Create your views here.


def rate_list(request):
    rates = Rate.objects.all()
    context = {
        'rates': rates
    }
    return render(request, 'Rates.html', context=context)


def contactus(request):
    contacts = ContactUs.objects.all()
    context = {
        'contacts': contacts
    }

    return render(request, 'contactUs.html', context=context)
