from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.utils.datastructures import MultiValueDictKeyError 

from .forms import UserCreationForm

def logout_view(request):
	logout(request)
	messages.success(request, "Why would you ever log out? That's it I'm giving you a computer virus")
	return HttpResponseRedirect(reverse('home'))

"""
You need to send and email with a link to a user authentication page
in order to confirm valid email
"""
class SignUpView(View):
	template_name = 'signup.html'
	form = UserCreationForm

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {'form': self.form})

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)

		if form.is_valid():
			save_it = form.save(commit=True)
			save_it.save()
			messages.success(request, 'thanks for joining asshole')
			return HttpResponseRedirect(reverse('account:thanks'))

class LoginView(View):
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
	template_name='logout.html'

class ThankYouView(TemplateView):
	template_name='thankyou.html'


