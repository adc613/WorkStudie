from django.contrib import admin
from .models import Task, Bid, Review

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
	pass

class BidAdmin(admin.ModelAdmin):
	pass

class ReviewAdmin(admin.ModelAdmin):
	pass

admin.site.register(Task, TaskAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Review, ReviewAdmin)