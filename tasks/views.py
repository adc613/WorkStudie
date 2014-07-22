import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView

from .forms import CreateTaskForm, CreateBidForm, CreateReviewForm
from .models import Task, Bid, Review
from workstudy.settings.base import EMAIL_HOST_USER

#view used when a studier accepts a given bid
@login_required
def accept_a_bid_view(request, **kwargs):
	task=Task.objects.get(pk=kwargs['task_pk'])
	
	if task.creator == request.user and task.accepted_bid == None:
		bid = Bid.objects.get(pk=kwargs['bid_pk'])
		task.accepted_bid = bid
		task.worker = bid.bidder
		task.accepted = True
		task.accepted_date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
		task.save()
		messages.success(request,"Congrats you've accepted a bid I'm proud of you")
		if bid.bidder.email_notifactions:
				send_mail('WorkStudie Notification',
					"Someone accepted your bid. Head over to WorkStudie.com to check it out",
					EMAIL_HOST_USER,
					[task.creator.email],
					fail_silently=False)
		return HttpResponseRedirect(reverse('task:task_list'))
	else:
		messages.error(request, """It looks as if this task has already been accepted
		 or maybe you're not the creator, but why would you being clicking 
		 buttons then... (The NSA is watchig you)
		 """)
		return HttpResponseRedirect(reverse('home'))

#View run when a task is outright accepted with out a bid or anything just accepted as is (worker would accept a task then this view woul run)
@login_required
def accept_task_view(request, **kwargs):
	if request.user.is_worker:
		task = Task.objects.get(pk=kwargs['pk'])
		bid = Bid.objects.create(
			bidder=request.user,
			bid = task.suggested_price,
			message = "This task was accepted by a worker as is, with no conditions attached."
			)
		bid.save()
		task.accepted_bid = bid
		task.worker = bid.bidder
		task.accepted = True
		task.accepted_date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
		task.save()
		if task.creator.email_notifictions:
				send_mail('WorkStudie Notification',
					"Someone accepted your task and it should be completely promptly. Head over to WorkStudie.com to check it out",
					EMAIL_HOST_USER,
					[task.creator.email],
					fail_silently=False) #Eventually I should changethis to True it's a minor thing not getting a notifaction and it'd be even more annoying to get an error message when the user is using the website

		messages.success(request,"You have taken on this task, please completely in a timely fasion.")
		return HttpResponseRedirect(reverse('home')) #Eventually this should be some sort of success page
	
	else:
		messages.error(request, "You are not worker therefore you're not allowed to accept the task")
		return HttpResponseRedirect(reverse('home'))# """I would like to change this at some point but for now it'll do later we can redirect to a differnt page"""

#creates a bid in order to bid on a task
class CreateBidView(View):
	form = CreateBidForm

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			save_it = form.save(commit=False)
			save_it.bidder = request.user
			save_it.save()

			task = Task.objects.get(pk=kwargs['pk'])
			bid = Bid.objects.get(pk=save_it.pk)
			task.bids.add(bid)

			if task.creator.email_notifactions:
				send_mail('WorkStudie Notification',
					"Someone bidded on your task. Head over to WorkStudie.com to check it out",
					EMAIL_HOST_USER,
					[task.creator.email],
					fail_silently=False)

			return HttpResponseRedirect(reverse('home'))

		else:
			return HttpResponseRedirect(reverse('task:task_list'))

#View that is run when a task is completed
@login_required
def complete_task_view(request, **kwargs):
	task=task.objects.get(pk=kwargs['task_pk'])
	if task.accepted == True and task.accepted_bid != None:
		
		if task.creator == request.user:
			
			task.completed = True
			review = Review.objects.get(pk=kwargs['review_pk'])
			task.worker_review = review
			task.completed_date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
			task.save()

			return HttpResponseRedirect(reverse('task:review', kwargs={'task_pk' : kwargs['task_pk']}))
		
		elif task.worker == request.user:
			
			review = Review.objects.get(pk=kwargs['review_pk'])
			task.creator_review = review
			task.completed_date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
			task.save()
			task.worker.profile.task_completed.add(task)
			return HttpResponseRedirect(reverse('task:review', kwargs={'task_pk' : kwargs['task_pk']}))
		
		else:
			
			messages.error(request, "You do not have permission to compelte task")
			return HttpResponseRedirect(reverse('home'))
	else:
		messages.error(request, "Bid has not acceted yet")
		HttpResponseRedirect(reverse('home'))

#This view is used when a task is completed and users are prompted to review each other
class CreateReviewView(View):
	form = CreateReviewForm
	template_name = 'createReview.html'

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			save_it = form.save(commit=False)
			save_it.creator = request.user
			save_it.save()
			task = Task.objects.get(pk=kwargs['task_pk'])
			task.worker_review = save_it
			task.completed = True
			task.save()
			return HttpResponseRedirect(reverse('task:task', pk=kwargs['task_pk']))

	@method_decorator(login_required)
	def get(self, request, **kwargs):
		return render(request,self.template_name, {'form': self.form, 'task_pk' : kwargs['task_pk']})

#View used to create task
class CreateTaskView(View):
	form = CreateTaskForm
	template_name = 'createTask.html'

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			save_it = form.save(commit=False)
			save_it.creator = request.user
			save_it.save()
			return HttpResponseRedirect('/account/thanks/')

	@method_decorator(login_required)
	def get(self, request):
		return render(request,self.template_name, {'form': self.form})

#detailed view of a task also where workers will bid on or accept tasks
class TaskDetailView(DetailView):
	model = Task
	template_name = 'taskDetail.html'
	form = CreateBidForm
	
	def get_context_data(self, **kwargs):
		context = super(TaskDetailView, self).get_context_data(**kwargs)
		context['now'] = timezone.now()
		task = self.model.objects.get(pk=self.kwargs['pk'])
		context['bids'] = task.bids.all()
		context['form'] = self.form
		context['accepted'] = task.accepted
		context['completed'] = task.completed
		context['bid'] = False if task.bids == None else False

		return context

class TaskDetailCreatorView(TaskDetailView):
	template_name = "taskDetailCreator.html"

class TaskDetailUserView(TaskDetailView):
	template_name = "taskDetailUser.html"

class TaskDetailWorkerView(TaskDetailView):
	template_name = "taskDetailWorker.html"

#redirects the user depending on the type of user they are this allows them to view the list of task in different ways
#for the worker for example there allowed to post bids accept the task.
def task_detail_view(request, **kwargs):
	task = Task.objects.get(pk=kwargs['pk'])
		
	if request.user.is_authenticated():
		if request.user == task.creator:
			return HttpResponseRedirect(reverse('task:task_detail_creator', kwargs={'pk':kwargs['pk']}))
		elif request.user == task.worker:
			return HttpResponseRedirect(reverse('task:task_detail_user', kwargs={'pk':kwargs['pk']})) #I need to change the user html document as is it doesn't make any sense
		elif request.user.is_worker == True:
			return HttpResponseRedirect(reverse('task:task_detail_worker', kwargs={'pk':kwargs['pk']}))
	else:	
		return HttpResponseRedirect(reverse('task:task_detail', kwargs={'pk':kwargs['pk']}))

#list all available task in the area
class TaskListView(ListView):
	model = Task
	form = CreateBidForm
	template_name = 'taskList.html'

	def get_queryset(self):
		return self.model.objects.filter(accepted=False)

	def get_context_data(self, **kwargs):
		context = super(TaskListView, self).get_context_data(**kwargs)
		context['now'] = timezone.now()
		context['form'] = self.form
		return context


