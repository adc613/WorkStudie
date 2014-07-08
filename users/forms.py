from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import	User


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password',
		widget = forms.PasswordInput)
	password2 = forms.CharField(label='repeat password',
		widget = forms.PasswordInput)

	class Meta:
		model =	User
		fields = ('email', 'first_name', 'last_name')

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password2 != password1:
			raiseforms.ValidationError('passwords do not match')
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model =	User
		fields = ('email', 'password', 'first_name', 'last_name', 'is_active',
			'is_superuser', 'is_worker')

	def clean_password(self):
		return self.initial['password']

