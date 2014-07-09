from django.conf.urls import patterns, include, url
from prototypes.app import views

urlpatterns = patterns('',
    url(r'$', views.prototype_listing, name='prototypes_listing'),
)
