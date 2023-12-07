from django.http import HttpResponseRedirect
from django.shortcuts import render

from currency.forms import SourceForm
from currency.models import Rate, ContactUs, Source


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


def source_create(request):
    if request.method == 'POST':
        form = SourceForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')

    else:
        form = SourceForm()

    context = {
        'form': form
    }
    return render(request, 'source_create.html', context=context)


def source_update(request, pk):
    source = Source.objects.get(source_id=pk)
    if request.method == 'POST':
        form = SourceForm(data=request.POST, instance=source)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')

    else:
        form = SourceForm(instance=source)

    context = {
        'form': form
    }
    return render(request, 'source_update.html', context=context)


def source_delete(request, pk):
    source = Source.objects.get(source_id=pk)
    if request.method == 'POST':
        source.delete()
        return HttpResponseRedirect('/source/list/')
    context = {
        'source': source
    }
    return render(request, 'source_delete.html', context=context)


def source_details(request, pk):
    source = Source.objects.get(source_id=pk)
    context = {
        'source': source
    }
    return render(request, 'source_details.html', context=context)


def source_list(request):
    sources = Source.objects.all()
    context = {
        'sources': sources
    }
    return render(request, 'source_list.html', context=context)
