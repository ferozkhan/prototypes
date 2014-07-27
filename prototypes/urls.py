from django.conf.urls import patterns, url
from prototypes.app import views


urlpatterns = patterns('',
    url(r'^prototypes/$', views.prototype_listing, name='prototypes_listing'),
    url(r'^prototypes/(?P<slug>[\w.\-]+)$', views.prototype_details, name='prototype_details')
)
