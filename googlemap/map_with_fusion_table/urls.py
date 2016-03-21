__author__ = 'ahsan'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^validate/$', views.validate_latlng, name='validate'),
]