
import os
from django import forms
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect


MAX_PROTOTYPE_LIMIT = 5242880
DEFAULT_PROTOTYPE = """
<!DOCTYPE html>
<html>
<head>
    <title>PROTOTYPE TITLE</title>
</head>
<body>
    PROTOTYPE BODY
</body>
</html>
"""


class PrototypeForm(forms.Form):
    name = forms.SlugField(label='name', max_length=15, min_length=3, required=True)
    prototype = forms.CharField(label='prototype', widget=forms.Textarea(attrs={
        'cols': 100, 'rows': 50
    }), required=True)

    def save(self, data):
        create_prototype(data)


def remove_prototype(request):
    if request.REQUEST.get('prototype'):
        prototype_path = os.path.join(settings.PROTOTYPE_DIR, request.REQUEST.get('prototype'))
        if os.path.exists(prototype_path):
            os.remove(prototype_path)
    return HttpResponseRedirect('/prototypes/')


def create_prototype(data):
    with open(os.path.join(settings.PROTOTYPE_DIR, data['name']), 'w+') as p:
        p.write(data['prototype'])


def prototype_listing(request):
    context = {}
    form = PrototypeForm(initial={'prototype': DEFAULT_PROTOTYPE})
    if request.method == 'POST':
        form = PrototypeForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if len(form_data['prototype']) > MAX_PROTOTYPE_LIMIT:
                raise forms.ValidationError('prototype size must be less than 5MB')
            form.save(form_data)

    context = {
        'prototypes': os.listdir(settings.PROTOTYPE_DIR),
        'form': form
    }
    return render(request, 'prototype-listing.html', context)


def prototype_details(request, slug):
    prototype = 'prototypes/{0}'.format(slug)
    return render(request, prototype)
