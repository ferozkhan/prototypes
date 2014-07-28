
import os
from django import forms
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect


default_prototype = """
<!DOCTYPE html>
<html>
<head>
    <title>PROTYPE TITLE</title>
</head>
<body>
    PROTYPE BODY
</body>
</html>
"""


def remove_prototype(request):
    if request.REQUEST.get('prototype'):
        if os.path.exists(os.path.join(settings.PROTOTYPE_DIR, request.REQUEST.get('prototype'))):
            os.remove(os.path.join(settings.PROTOTYPE_DIR, request.REQUEST.get('prototype')))
    return HttpResponseRedirect('/prototypes/')


def create_prototype(data):
    with open(os.path.join(settings.PROTOTYPE_DIR, data['name']), 'w+') as p:
        p.write(data['prototype'])
    return HttpResponseRedirect('/prototypes/')


class PrototypeForm(forms.Form):
    name = forms.CharField(label='name', max_length=15, min_length=3, required=True)
    prototype = forms.CharField(label='prototype', widget=forms.Textarea(attrs={
        'cols': 100, 'rows': 50
    }), required=True)

    def save(self, data):
        return create_prototype(data)


def prototype_listing(request):
    context = {}
    form = PrototypeForm(initial={'prototype': default_prototype})
    if request.method == 'POST':
        form = PrototypeForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['name'] = form_data['name'] + '.html'
            form.save(form_data)

    context = {
        'prototypes': os.listdir(settings.PROTOTYPE_DIR),
        'form': form
    }
    print context
    return render(request, 'prototype-listing.html', context)


def prototype_details(request, slug):
    prototype = 'prototypes/{0}'.format(slug)
    return render(request, prototype)
