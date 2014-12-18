from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', homepage_view, name='home'),
    url(r'^about/$', about_us_view, name='about_us'),
    url(r'^thankyou/$', ThankYouView.as_view(), name='thanks'),
    
    url(r'^account/', include('users.urls', namespace='users')),
    url(r'^tasks/', include('tasks.urls', namespace='tasks')),
    url(r'^checkout/', include('checkout.urls', namespace='checkout')),

    
   url(r'^admin/', include(admin.site.urls)),
)
