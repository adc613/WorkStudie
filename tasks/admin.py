from django.contrib import admin
from .models import Task, Bid, Review

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
	"""	
	list_display = ('title', 'is_accepted', 'is_completed', 
		'worker','studier')
	list_filer = ('is_completed', 'is_accepted')
	"""
	pass

class BidAdmin(admin.ModelAdmin):
	pass

class ReviewAdmin(admin.ModelAdmin):
	pass

admin.site.register(Task, TaskAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Review, ReviewAdmin)