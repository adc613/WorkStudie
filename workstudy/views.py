from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.
def homepage_view(request):
	"""
	View of the home page
	"""
	template_name = 'homepage.html'
	return render(request, template_name)

def about_us_view(request):
	"""
	View of the about us page
	"""
	template_name = "about_us.html"
	return render(request, template_name)

class ThankYouView(TemplateView):
	"""
	View of the thank your page thsi is the second thank you page views
	i've seen could be violationg DRY
	"""
	template_name='thankyou.html'