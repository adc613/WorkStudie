from django import forms

from .models import Task, Bid, Review

class CreateTaskForm(forms.ModelForm):
	"""
	Creates a Task
	"""
 	class Meta:
 		model = Task
 		fields = ['title', 'discription', 'suggested_price']

class CreateBidForm(forms.ModelForm):
	"""
	Creates a bid.
	"""
 	class Meta:
 		model = Bid
 		fields = ['bid', 'message']

class CreateReviewForm(forms.ModelForm):
	"""
	Creates a review.
	"""
	class Meta:
		model = Review
		fields = ['rating', 'comments']

