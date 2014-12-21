import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

class IntegerRangeField(models.IntegerField):
	"""
	A integer field that can only have a value between a given min and max
	"""
	def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
		self.min_value, self.max_value = min_value, max_value
		models.IntegerField.__init__(self, verbose_name, name, **kwargs)
	def formfield(self, **kwargs):
		defaults = {'min_value': self.min_value, 'max_value':self.max_value}
		defaults.update(kwargs)
		return super(IntegerRangeField, self).formfield(**defaults)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([
        (
            (IntegerRangeField, ),
            [],
            {
                "verbose_name": ["verbose_name", {"default": None}],
                "name":         ["name",         {"default": None}]
            },
        ),
    ], ["^tasks\.models\.IntegerRangeField"])

class Review(models.Model):
	"""
	A review for a worker or studier meant to be compeleted after every task.
	"""
	#the rating of the opposite party
	rating = IntegerRangeField(min_value=1, max_value=10)
	#Any extra cmments thhey may have
	comments = models.TextField(max_length=1000, blank=True)
	#the Creator the review
	creator = models.ForeignKey('users.User', related_name="review_creator",
	 null=True, blank=True)

	def __unicode__(self):
		return self.creator

class Bid(models.Model):
    """
    Bid is used to bid on a task if for example the suggested price was set too 
    high by the worker or there is no suggested price.
    """
    #Bidding price
    bid = models.DecimalField(max_digits=5, decimal_places=2)
	#The bidder
    bidder = models.ForeignKey('users.User', null=False, blank=False)
	#A message meant for the creator about why there qualified or any specail conditions or anything really
    message = models.TextField(max_length=140, blank=True)
    #The task being bidded on
    task = models.ForeignKey('tasks.Task', related_name='bid') 

    def __unicode__(self):
        return self.bidder


class Task(models.Model):
    """
    A task is the foundation of this site represents a task posted by a studier
    that needs to be complted.
    """
    #Title of the task
    title = models.CharField(blank=False, max_length=75)
	#discription of the actual task
    discription = models.TextField(blank=False, max_length=420) 
	#the price that the studier is willing to pay, not necessairly maximum price
    suggested_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
	
	#Boolean field should be false until a worker accpets the task
    accepted = models.BooleanField(default=False)
	#Boolean fileds should reamin false until the task is completed and transation is done
    completed = models.BooleanField(default=False)
	#Foreign Key represents the author of the tasks
    creator = models.ForeignKey('users.User', related_name='task_creator')
	#A foreign ket that represents only the worker who has accpeted the task
    worker = models.ForeignKey('users.User', limit_choices_to={'is_worker' : True}, related_name='task_worker', null=True, blank=True)
	
	#A field to represent the selected bid for the task
    accepted_bid = models.ForeignKey(Bid, related_name='accepted_bid', null=True, blank=True)
	#Review given made by the worker about the creator
    worker_review = models.ForeignKey(Review, related_name='task_worker_review', null=True, blank=True)
	#review made by the creator about the worker
    creator_review = models.ForeignKey(Review, related_name='task_create_review', null=True, blank=True)

	#date created
    creation_date = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False, null=True)
	#the date that the task was accepted
    acception_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
	#the date that the task was completed
    completion_Date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)

    objects = TaskManager()

    def accept_bid(self,bid):
        if self.accepted_bid:
            raise ValidationError('a bid has already been accepted')
        else:
            self.accepted_bid = bid
            self.worker = bid.bidder
            self.accepted = True
            self.accepted_date = datetime.datetime.utcnow()
            self.save()
            return True

	#returns url of the detail view for the task	
    def get_absolute_url(self):
        return reverse('tasks:task', kwargs={'pk' : self.pk})

    def __unicode__(self):
        return self.title
