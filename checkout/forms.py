from django import forms

class CreditCardInfo(forms.Form):
	"""
	Form for puting in credit card info 
	"""
	card_number = forms.IntegerField(max_value=9999999999999999, min_value=99999999999999)
	cvv = forms.IntegerField(max_value=999, min_value=99)
	expiration_month = forms.IntegerField(max_value=13, min_value=0)
	expiration_year = forms.IntegerField(max_value=2030, min_value=2013)
	first_name = forms.CharField(max_length=255)
	last_name = forms.CharField(max_length=255)
	street_address = forms.CharField(max_length=255)
	city = forms.CharField(max_length=255)
	state = forms.CharField(max_length=255)
	zip_code = forms.CharField(max_length=255)
	country = forms.CharField(max_length=255)
	phone = forms.CharField(max_length=255)