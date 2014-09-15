from django.conf.urls import patterns, include, url

from .views import *

urlpatterns = patterns('',
	url(r'^createtask/$', CreateTaskView.as_view(), name='create_task'),
	
	url(r'^task/(?P<pk>\d+)/$', task_detail_view, name = 'task'),
	url(r'^taskcreator/(?P<pk>\d+)/$', TaskDetailCreatorView.as_view(), name = 'task_detail_creator'),
	url(r'^taskworker/(?P<pk>\d+)/$', TaskDetailWorkerView.as_view(), name = 'task_detail_worker'),
	url(r'^taskuser/(?P<pk>\d+)/$', TaskDetailUserView.as_view(), name = 'task_detail_user'),
	url(r'^taskanonymous/(?P<pk>\d+)/$', TaskDetailView.as_view(), name = 'task_detail'),
	
	url(r'^list/$', TaskListView.as_view(), name='task_list'),
	url(r'^bid/(?P<pk>\d+)/$', CreateBidView.as_view(), name='create_bid'),
	url(r'^heysoulsister/(?P<task_pk>\d+)/(?P<bid_pk>\d+)/$', accept_a_bid_view, name='accept_bid'),
	url(r'^accepttask/(?P<pk>\d+)/$', accept_task_view, name='accept_task' ),
	
	url(r'^completetask/(?P<task_pk>\d+)/(?P<review_pk>\d+)/$', complete_task_view, name='complete_task'),
	url(r'^createreview/(?P<task_pk>\d+)/$', CreateReviewView.as_view(), name='create_review'),

)