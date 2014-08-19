
import os
from django import forms
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.template import TemplateDoesNotExist


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
        prototypes_dir = getattr(settings, 'PROTOTYPE_DIR', None)
        if not os.path.exists(prototypes_dir):
            os.mkdir(prototypes_dir)
        with open(os.path.join(prototypes_dir, data['name']), 'w+') as p:
            p.write(data['prototype'])


def remove_prototype(request):
    proto_name = request.REQUEST.get('prototype', None)
    if proto_name:
        if os.path.exists(os.path.join(getattr(settings, 'PROTOTYPE_DIR', None), proto_name)):
            os.remove(os.path.join(settings.PROTOTYPE_DIR, proto_name))
    return HttpResponseRedirect('/prototypes/')


def prototype_listing(request):
    context = {}
    form = PrototypeForm(initial={'prototype': DEFAULT_PROTOTYPE})
    if request.method == 'POST':
        try:
            form = PrototypeForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                if len(form_data['prototype']) > MAX_PROTOTYPE_LIMIT:
                    raise forms.ValidationError('prototype size must be less than 5MB')
                form.save(form_data)
        except Exception, ex:
            form.errors['error'] = ':  ' + ex.message

    context = {
        'prototypes': os.listdir(settings.PROTOTYPE_DIR),
        'form': form
    }
    return render(request, 'prototype-listing.html', context)


def prototype_details(request, slug):
    try:
        prototype = 'prototypes/{0}'.format(slug)
        return render(request, prototype)
    except TemplateDoesNotExist:
        raise Http404
