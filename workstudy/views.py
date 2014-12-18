from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.
class ThankYouView(TemplateView):
	"""
	View of the home page
	"""
	template_name = 'workstudy/homepage.html'

class ThankYouView(TemplateView):
	"""
	View of the about us page
	"""
	template_name = "workstudy/hbout_us.html"

class ThankYouView(TemplateView):
	"""
	View of the thank your page thsi is the second thank you page views
	i've seen could be violationg DRY
	"""
	template_name='workstudy/thankyou.html'
