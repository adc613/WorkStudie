from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.class UserManager(BaseUserManager):
class Profile(models.Model):
	"""
	Represents every users profile.
	"""
	#All the task that have been made by this user
	tasks_made = models.ManyToManyField('tasks.Task', related_name='task_made')
	#All the task that have been completed by the user
	tasks_completed = models.ManyToManyField('tasks.Task', related_name='tasks_completed')
	#Discription of what skills that have
	description = models.TextField(max_length='1000', blank=True)
	#Intended Major
	intended_major = models.CharField(max_length=255, blank=True, default="Life")

class UserManager(BaseUserManager):	
	"""
	Stolen code from online
	"""

	def create_user(self, email, first_name='John',last_name='Doe', password= None):
		if not email:
			raise ValueError('User must have email')

		user = self.model(
			email=self.normalize_email(email),
			first_name=first_name,
			last_name=last_name
		)

		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password, first_name='', last_name=''):
		user = self.create_user(email, first_name, last_name, password=password)
		user.is_admin = True
		user.is_superuser = True
		user.is_worker = True
		user.is_active = True
		user.save()
		return user

class User(AbstractBaseUser, PermissionsMixin):
	"""
	Represents every user just with different permissions
	"""
	#date that user join
	creation_date = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
	#link to user profile
	profile = models.ForeignKey(Profile, null=True, blank=True, related_name='user_profile') #bad code
	email = models.EmailField(max_length=100, unique=True, primary_key=True)
	first_name = models.CharField(max_length=255, blank=False)
	last_name = models.CharField(max_length=100, blank=False)
	is_active = models.BooleanField(default=False)
	merchant_account_id = models.CharField(max_length=255, null=True)
	
	is_admin = models.BooleanField(default=False)
	is_worker = models.BooleanField(default=False)
	email_notifictions = models.BooleanField(default=True)
	is_superuser = False
	
	objects = UserManager()

	USERNAME_FIELD = 'email'

	def make_worker(self):
		self.is_worker = True
		return self

	def get_full_name(self):
		return self.first_name +' ' + self.last_name

	def get_short_name(self):
		return self.first_name

	def __unicode__(self):
		return self.email

	@property
	def is_staff(self):
		return self.is_superuser		



