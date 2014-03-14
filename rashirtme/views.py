"""
Django views for rashirtme project.

"""

from django.shortcuts import render
from django.http.response import HttpResponse


def home(request):
    """    Display the Landing Page    """

    context = {
        'stripe_publishable_key': 'pk_test_qZ3TjohtOSXEeXhPubJgY64y',
        'shirt_price': '20',
    }

    return render(request, 'home.html', context)


def process_order(request):
    """    Process the Incoming Order    """

    print request.POST

    return HttpResponse('Working!')