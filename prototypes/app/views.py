
import os
import sys
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def prototype_listing(request):
    context = {}
    context['prototypes'] = os.listdir(settings.PROTOTYPE_DIR)
    return render(request, 'prototype-listing.html', context)


def prototype_details(request, slug):
    prototype = 'prototypes/{0}'.format(slug)
    return render(request, prototype, dirs=(settings.PROTOTYPE_DIR))