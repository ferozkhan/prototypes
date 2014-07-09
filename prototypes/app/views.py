
import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

def prototype_listing(request):
    context = {}
    templates = os.listdir(settings.PROTOTYPE_DIR)
    context['templates'] = templates
    return render(request, 'prototype-listing.html', context)
