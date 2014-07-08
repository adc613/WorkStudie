from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', homepage_view, name='home'),
    url(r'^about/$', about_us_view, name='about_us'),
    url(r'^account/', include('users.urls', namespace='account')),
    url(r'^tasks/', include('tasks.urls', namespace='task')),

    
    url(r'^admin/', include(admin.site.urls)),
)
