from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView


from .forms import CreateTaskForm, CreateBidForm, CreateReviewForm
from .models import Task, Bid, Review

@login_required
def complete_task_view(request, **kwargs):
	task=task.objects.get(pk=kwargs['task_pk'])
	if task.accepted == True and task.accepted_bid != None:
		if task.creator == request.user:
			task.completed = True
			review = Review.objects.get(pk=kwargs['review_pk'])
			task.worker_review = review
			task.save()
			return HttpResponseRedirect(reverse('task:review', kwargs={'task_pk' : kwargs['task_pk']}))
		elif task.worker == request.user:
			review = Review.objects.get(pk=kwargs['review_pk'])
			task.creator_review = review
			task.save()
			return HttpResponseRedirect(reverse('task:review', kwargs={'task_pk' : kwargs['task_pk']}))
		else:
			messages.error(request, "You do not have permission")
			return HttpResponseRedirect(reverse('home'))
	else:
		messages.error(request, "Bid has not acceted yet")
		HttpResponseRedirect(reverse('home'))

@login_required
def accept_a_bid_view(request, **kwargs):
	task=Task.objects.get(pk=kwargs['task_pk'])
	
	if task.creator == request.user and task.accepted_bid == None:
		bid = Bid.objects.get(pk=kwargs['bid_pk'])
		task.accepted_bid = bid
		task.worker = bid.bidder
		task.accepted = True
		task.save()
		messages.success(request,"Congrats you've accepted a bid I'm proud of you")
		return HttpResponseRedirect(reverse('task:task_list'))
	else:
		messages.error("""It looks as if this task has already been accepted
		 or maybe you're not the creator, but why would you being clicking 
		 buttons then... (The NSA is watchig you)
		 """)
		return HttpResponseRedirect(reverse('home'))

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

def test_view(request, **kwargs):
	return HttpResponseRedirect(reverse('task:task_detail_creator', kwargs={'pk':1}))



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
		return context


class TaskDetailCreatorView(TaskDetailView):
	template_name = "taskDetailCreator.html"

class TaskDetailUserView(TaskDetailView):
	template_name = "taskDetailUser.html"

class TaskDetailWorkerView(TaskDetailView):
	template_name = "taskDetailWorker.html"

def task_detail_view(request, **kwargs):
	template_name = 'taskDetail.html'
	task = Task.objects.get(pk=kwargs['pk'])
		
	if request.user.is_authenticated():
		if request.user == task.creator:
			return HttpResponseRedirect(reverse('task:task_detail_creator', kwargs={'pk':kwargs['pk']}))
		if request.user == task.worker:
			return HttpResponseRedirect(reverse('task:task_detail_user', kwargs={'pk':kwargs['pk']}))
		if request.user.is_worker == True:
			return HttpResponseRedirect(reverse('task:task_detail_worker', kwargs={'pk':kwargs['pk']}))
		
	return HttpResponseRedirect(reverse('task:task_detail', kwargs={'pk':kwargs['pk']}))


class TaskListView(ListView):
	model = Task
	form = CreateBidForm
	template_name = 'taskList.html'

	def get_quereyset(self):
		return self.model.objects.filter(accepted=False)

	def get_context_data(self, **kwargs):
		context = super(TaskListView, self).get_context_data(**kwargs)
		context['now'] = timezone.now()
		context['form'] = self.form
		return context

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

			return HttpResponseRedirect(reverse('home'))

		else:
			return HttpResponseRedirect(reverse('task:task_list'))
