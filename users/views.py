from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.mail import mail_admins
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.utils.datastructures import MultiValueDictKeyError 


from .forms import UserCreationForm, ProfileCreationForm
from .models import Profile, User

def logout_view(request):
	"""
	Will logout the user and redirect to the homepage
	"""
	logout(request)
	messages.success(request, "Why would you ever log out? That's it I'm giving you a computer virus")
	return HttpResponseRedirect(reverse('home'))

"""
You need to send and email with a link to a user authentication page
in order to confirm valid email
"""
class ApplicationView(View):
	"""
	Is an application do joine workstudie, I think everything is really completed in the worker application
	and the studier application.
	"""
	template_name = "application.html"

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {})

class StudierApplicationView(View):
	"""
	An application for a studier to just workstudie
	"""
	template_name = 'applicationStudier.html'
	form = UserCreationForm

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {'form': self.form})

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)

		if form.is_valid():
			save_it = form.save(commit=True)
			save_it.save()
			mail_admins(
				'Studier Application', 
				'%s wants to become a studier. Their email is %s' % (save_it.first_name, save_it.email),
				fail_silently=False,
				)
			messages.success(request, 'thanks for joining asshole')
			return HttpResponseRedirect(reverse('account:thanks'))

class WorkerApplicationView(View):
	"""
	An application to just workstudie as a worker
	"""
	template_name = 'applicationWorker.html'
	form = UserCreationForm

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {'form': self.form})

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)

		if form.is_valid():
			save_it = form.save(commit=True)
			save_it.save()
			mail_admins(
				'Worker Application', 
				'%s wants to become a worker. Their email is %s' % (save_it.first_name, save_it.email),
				fail_silently=False,
				)
			messages.success(request, 'thanks for joining asshole')
			return HttpResponseRedirect(reverse('account:thanks'))

		messages.error(request, 'There was a problem with your application')
		return HttpResponseRedirect(reverse('account:thanks'))

class LoginView(View):
	"""
	Logs user into the website
	"""
	template_name = 'login.html'

	def get(self,request):
		return render (request, self.template_name, {})

	def post(self, request, *args, **kwargs):
		username = request.POST['email']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				messages.success(request, 'YOU DID IT! YOU LOGGED IN! I KNEW YOU COULD DO IT! I BET YOUR MOTHER IS SO PROUD!!!')
				return HttpResponseRedirect(reverse('home'))
			else:
				messages.success(request, "UH OH! you ain't active please leave")
				return HttpResponseRedirect(reverse('home'))

		else:
			messages.success(request, 'UH OH! you did something wrong please leave')
			return HttpResponseRedirect(reverse('home'))


class PostLogoutView(TemplateView):
	"""
	This is where all logoed out users get redirected
	"""
	template_name = 'logout.html'

class ThankYouView(TemplateView):
	"""
	Standard thank you page that is used for most thank users for differnt things with
	custom messages.
	"""
	template_name = 'thankyou.html'

class CreateProfileView(View):
	"""
	A view that allows the user to create his or her profile
	"""
	form = ProfileCreationForm
	template_name = 'createProfile.html'

	@method_decorator(login_required)
	def get(self, request):
		return render(request, self.template_name, {'form' : self.form})

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			user = request.user
			save_it = form.save(commit=False)
			user.profile = save_it
			save_it.save()
			user.save()
			messages.success(request, "You created your profile")
			return HttpResponseRedirect(reverse('account:thanks'))


class MyProfileView(View):
	"""
	Shows the user profile
	"""
	template_name = 'profile.html'

	def get(self, request):
		user = request.user
		if user.profile== None:
			HttpResponseRedirect(reverse('account:create_profile'))
		profile = user.profile
		number_of_completed_task = profile.tasks_completed.count()
		number_of_task_made = profile.tasks_made.count()
		context = {'user': user, 
			'profile':profile,
			'major':profile.intended_major,
			'tasks_completed' : number_of_completed_task,
			'tasks_made' : number_of_task_made
			}
		return render(request, self.template_name, context)

class ProfileView(DetailView):
	"""
	This calss might be excessive not sure yet tho so I'lll leave it
	Not entirely postive what it's for
	"""
	model = Profile
	template_name = 'profile.html'

	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)
		profile = Profile.objects.get(pk = self.kwargs['pk'])
		user = profile.user
		number_of_completed_task = profile.tasks_completed.count()
		number_of_task_made = profile.tasks_made.count()
		context = {'user': user, 
			'profile':profile,
			'major':profile.intended_major,
			'tasks_completed' : number_of_completed_task,
			'tasks_made' : number_of_task_made
			}
		return context

