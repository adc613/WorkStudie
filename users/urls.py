from django.conf.urls import patterns, include, url

from .views import *

urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^byebye/$', PostLogoutView.as_view(), name='post_logout'),
    url(r'^application/$', ApplicationView.as_view(), name='application'),
    url(r'^IWannaWork/$', WorkerApplicationView.as_view(), name='worker_application'),
    url(r'^IWannaStidoe/$', StudierApplicationView.as_view(), name='studier_application'),
    url(r'^MyProfile/$', MyProfileView.as_view(), name='my_profile'),
    url(r'^profile/(?P<pk>\d+)/', ProfileView.as_view(), name='profile'),
    url(r'^createprofile/$', CreateProfileView.as_view(), name='create_profile')
)
