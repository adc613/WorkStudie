from django.conf.urls import patterns, include, url

from .views import *

urlpatterns = patterns('',
	url(r'^test/(?P<pk>\d+)/$', CheckoutView.as_view() , name = 'checkout')
)