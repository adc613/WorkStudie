from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User, Profile
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(UserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'first_name','last_name',
		'is_active', 'is_superuser', 'is_worker', 'email_notifictions',
		'profile')
	list_filter = ('is_superuser','is_admin', 'is_worker')

	fieldsets = (
		(None, {'fields' : (
		'email', 'first_name','last_name', 'password', 'is_superuser', 'is_active', 'is_worker',
		 'email_notifictions', 'profile')
		}), ('Groups', {'fields' :('groups',)})
		)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields' : {'email', 'first_name','last_name', 'password1', 'password2'}
			}
		),
	)

	search_fields = ('email', 'first_name', 'last_name')
	ordering = ('last_name',)

class ProfileAdmin(admin.ModelAdmin):
	pass

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
