from django.conf.urls import patterns, include, url

from .views import *

urlpatterns = patterns('',
	url(r'^test/(?P<pk>\d+)/$', CheckoutView.as_view() , name = 'checkout'),
	url(r'^p/$', CheckoutView.as_view() , name = 'p'),
	url(r'^t/$', t.as_view() , name = 't'),
)