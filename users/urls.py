from django.conf.urls import patterns, include, url

from .views import *

urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^byebye/$', PostLogoutView.as_view(), name='post_logout'),
    url(r'^thanks/$', ThankYouView.as_view(), name='thanks'),
    url(r'^signup/$', SignUpView.as_view(), name='signup')
)
