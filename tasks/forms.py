from django import forms

from .models import Task, Bid, Review

class CreateTaskForm(forms.ModelForm):
 	class Meta:
 		model = Task
 		fields = ['title', 'discription']

class CreateBidForm(forms.ModelForm):
 	class Meta:
 		model = Bid
 		fields = ['bid', 'message']

class CreateReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['rating', 'comments']

