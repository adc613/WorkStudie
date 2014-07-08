from django.shortcuts import render

# Create your views here.
def homepage_view(request):
	template_name = 'homepage.html'
	return render(request, template_name)

def about_us_view(request):
	template_name = "about_us.html"
	return render(request, template_name)