"""
Django views for rashirtme project.

"""

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound
from rashirtme.apps.shop.forms import OrderForm
from django.conf import settings


def home(request):
    """    Display the Landing Page    """

    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLIC_KEY,
        'shirt_price': settings.SHIRT_PRICE,
    }

    return render(request, 'home.html', context)


def process_order(request):
    """    Process the Incoming Order    """

    form = OrderForm(data=request.POST or None, files=request.FILES or None)

    if form.is_valid():
        form.save()
        return HttpResponse('Success!\n')
    else:
        print form.errors
        return HttpResponseNotFound('Working!')