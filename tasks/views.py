import datetime

from django.core.exceptions import PermissionDenied
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
from users.models import Profile 
from workstudy.settings import EMAIL_HOST_USER

#view used when a studier accepts a given bid
@login_required
def accept_a_bid_view(request, **kwargs):
    """
    Function is run in order to accept a bid. It the user is not the creator
    of the task it should throw an error. Also will send creator an email
    notifying them that their bid was accepted and they should promptly completely
    the task.
    """
    task=Task.objects.get(pk=kwargs['task_pk'])
    
    if task.creator == request.user:
        bid = Bid.objects.get(pk=kwargs['bid_pk'])
        ok = task.accept_bid(bid)
        if ok:
            messages.success(request,"Congrats you've accepted a bid I'm proud of you")
            if bid.bidder.email_notifactions:
                 send_mail('WorkStudie Notification',
                        "Someone accepted your bid. Head over to WorkStudie.com to check it out",
                        EMAIL_HOST_USER,
                        [task.creator.email],
                        fail_silently=False)
            return HttpResponseRedirect(reverse('tasks:task_list'))
        else:    
            messages.error(request, 
            """
            There was a problem accepted your task, most likely another bid
            was already accepted but if you don't believe this to be the case
            please try again. If porblem continues contact workstudie@gmail.com.
            """)
            return HttpResponseRedirect(reverse('home'))

    else:
        messages.error(request, """It looks as if this task has already been accepted
         or maybe you're not the creator, but why would you being clicking 
         buttons then... (The NSA is watchig you)
         """)
        return HttpResponseRedirect(reverse('home'))

#View run when a task is outright accepted with out a bid or anything just accepted as is (worker would accept a task then this view woul run)
@login_required
def accept_task_view(request, **kwargs):
    """
    This function is run when a worker accepts a task just as the studier required and
    at the studier's suggested price. The Studier should be notfied that their task was
    accepted and a work will complete promptly.
    """
    if request.user.is_worker:
        task = Task.objects.get(pk=kwargs['pk'])
        bid = Bid.objects.create(
            task=task,
            bidder=request.user,
            bid = task.suggested_price,
            message = "This task was accepted by a worker as is, with no conditions attached."
            )
        task.accept_bid(bid)
        if task.creator.email_notifactions:
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
    """
    View used for a worker creating a bid on a specfic task. 
    """

    form = CreateBidForm
    template_name = "tasks/createBid.html"

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        if request.user.is_worker:
            context = {'pk':kwargs['pk'], 'form':self.form}
            return render(request, self.template_name, context)
        else:
            raise PermissionDenied("Only wokers can bid on task")


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.user.is_worker:
            form = self.form(request.POST or None)
            if form.is_valid():
                task = Task.objects.get(pk=kwargs['pk'])
                save_it = form.save(commit=False)
                save_it.bidder = request.user
                save_it.task = task
                save_it.save()

                if task.creator.email_notifactions:
                    send_mail('WorkStudie Notification',
                        "Someone bidded on your task. Head over to WorkStudie.com to check it out",
                        EMAIL_HOST_USER,
                        [task.creator.email],
                        fail_silently=False)

                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request,
                        """
                        Form was in valid please try again. If porblem continues
                        please contact workstudie@gmail.com.
                        """)
                return HttpResponseRedirect(reverse('tasks:create_bid',
                    kwargs={'pk':kwargs['pk']}))
        else:
            raise PermissionDenied("Only workers can bid on task")

#View that is run when a task is completed need to redirect to checkout
@login_required
def complete_task_view(request, **kwargs):
    """
    Completes the task and eventually should redirect to the payment processing
    Both the worker and the studier must complete the task it also redirects them 
    to the review page where both worker and studier review each other.
    """

    task=task.objects.get(pk=kwargs['task_pk'])
    if task.accepted == True and task.accepted_bid != None:
        
        if task.creator == request.user:
            if not task.review_of_worker:
                messages.error("Please complete review")
                return HttpResponseRedirect(reverse('tasks:create_review'))
            task.completed = True
            review = Review.objects.get(pk=kwargs['review_pk'])
            task.worker_review = review
            task.completed_date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
            task.save()

            return HttpResponseRedirect(reverse('tasks:review', kwargs={'task_pk' : kwargs['task_pk']}))
        
        elif task.worker == request.user:
            
            if not task.review_of_creator:
                message.error("Please complete review")
                return HttpResponseRedirect(reverse('tasks:create_review'))
            review = Review.objects.get(pk=kwargs['review_pk'])
            task.creator_review = review
            task.completed_date = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
            task.save()
            task.worker.profile.task_completed.add(task)
            return HttpResponseRedirect(reverse('tasks:review', kwargs={'task_pk' : kwargs['task_pk']}))
        
        else:
            
            messages.error(request, "You do not have permission to compelte task")
            return HttpResponseRedirect(reverse('home'))
    else:   
        messages.error(request, "Bid has not acceted yet")
        HttpResponseRedirect(reverse('home'))

#This view is used when a task is completed and users are prompted to review each other
class CreateReviewView(View):
    """
    This view is used to create a new review on a worker or studier based on how well they
    performed or how conciderate they were when doing the task.
    """
    form = CreateReviewForm
    template_name = 'tasks/createReview.html'

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        return render(request,self.template_name, {'form': self.form, 'task_pk' : kwargs['task_pk']})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['task_pk'])
        if request.user != task.worker and request.user != task.creator:
            raise PermissionDenied("You are not allowed to review this task")
        form = self.form(request.POST or None)
        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.creator = request.user
            save_it.save()
            task = Task.objects.get(pk=kwargs['task_pk'])
            if request.user == task.worker:
                task.review_of_creator= save_it
                task.save()
            else :
                task.review_of_worker = save_it
                task.save()
            return HttpResponseRedirect(reverse('tasks:task', kwargs={'pk':kwargs['task_pk']}))
        messages.error(request,
                """
                There's been a mistaek with your review, please try again, if
                there continues to be a problem please email WorkStudie@gmail.com
                """
                )
        return HttpResponseRedirect(reverse('tasks:task', kwargs={'pk':kwargs['task_pk']}))

    

#View used to create task
class CreateTaskView(View):
    """
    View used to create a task.
    """
    form = CreateTaskForm
    template_name = 'tasks/createTask.html'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        if form.is_valid():
            user = request.user
            save_it = form.save(commit=False)
            save_it.creator = user
            save_it.save()
            return HttpResponseRedirect(reverse('thanks'))

    @method_decorator(login_required)
    def get(self, request):
        return render(request,self.template_name, {'form': self.form})

#detailed view of a task also where workers will bid on or accept tasks
class TaskDetailView(DetailView):
    """
    Shows the details of a task. And acts a base class for the other detail views
    Other classes extended this in order to use a different template with varying
    amount of information or options.
    """
    model = Task
    template_name = 'tasks/taskDetail.html'
    form = CreateBidForm
    
    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        task = self.model.objects.get(pk=self.kwargs['pk'])
        context['bids'] = task.bids.all()
        context['accepted'] = task.accepted
        context['completed'] = task.completed
        context['bid'] = False if task.bids == None else False

        return context

class TaskDetailCreatorView(TaskDetailView):
    """
    View shows the creator their detailed view of their task.
    """
    template_name = "tasks/taskDetailCreator.html"

class TaskDetailUserView(TaskDetailView):
    """
    View Shows a random user their detialed view of a task.
    """
    template_name = "tasks/taskDetailUser.html"

class TaskDetailWorkerView(TaskDetailView):
    """
    View shows the worker their detailed view of a task.
    """
    template_name = "tasks/taskDetailWorker.html"

class BidView(TaskDetailView):
    """
    I think this is meant to show all the bids for a task, but I'm not entirely
    sure...
    """
    model = Task
    template_name = 'tasks/taskBid.html'
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


def task_detail_view(request, **kwargs):
    """
    Redirects the user to their proper view depending on what kind of user they
    are.
    """
    task = Task.objects.get(pk=kwargs['pk'])
        
    if request.user.is_authenticated():
        if request.user == task.creator:
            return HttpResponseRedirect(reverse('tasks:task_detail_creator', kwargs={'pk':kwargs['pk']}))
        elif request.user == task.worker:
            return HttpResponseRedirect(reverse('tasks:task_detail_user', kwargs={'pk':kwargs['pk']})) #I need to change the user html document as is it doesn't make any sense
        elif request.user.is_worker == True:
            return HttpResponseRedirect(reverse('tasks:task_detail_worker', kwargs={'pk':kwargs['pk']}))    
    
    return HttpResponseRedirect(reverse('tasks:task_detail', kwargs={'pk':kwargs['pk']}))

#list all available task in the area
class TaskListView(ListView):
    """
    List all available task (all task that have yet to be accpeted by the studier)
    """
    model = Task
    form = CreateBidForm
    template_name = 'tasks/taskList.html'

    def get_queryset(self):
        return self.model.objects.filter(accepted=False)

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['form'] = self.form
        return context

class UserTaskListView(ListView):
    """
    List all task with respect to one user
    """
    model = Task
    template_name = 'tasks/taskList.html'

    def get_queryset(self):
        #try:
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk = pk)
        return profile.tasks_made.all()         
        """
        except KeyError:
            pk = self.request.user.profile.pk

            profile = Profile.objects.get(pk = pk)

            return profile.tasks_made.all()         
"""



