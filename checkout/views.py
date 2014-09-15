from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.shortcuts import render

import braintree

from forms import CreditCardInfo
from tasks.models import Task

# Create your views here.
class CheckoutView(View):
	"""
	Will checkout user and add the correct amount of money
	to their wallets.
	"""
	template_name = "test.html"
	credit_card_form = CreditCardInfo
	def get(self, request, **kwrags):
		task = Task.objects.get(pk=kwargs['pk'])
		if not request.user == task.creator:
			messages.error("what are you doing I see you")
			return HttpResponseRedirect(reverse('home'))
		return render(request, self.template_name, 
			{'credit_card_form' : self.credit_card_form})

	def post(self, request, *args, **kwrags):
		task = Task.objects.get(pk=kwargs['pk'])
		if not request.user == task.creator:
			messages.error("what are you doing I see you")
			return HttpResponseRedirect(reverse('home'))
		credit_card = self.credit_card_form(request.POST or None)
		if not credit_card.is_valid():
			messages.error(request, "credit card form is not valid")
			return HttpResponseRedirect(reverse('home'))

		amount = task.accepted_bid.bid
		service_fee = amount*.2

		result = braintree.Transaction.sale({
        	"merchant_account_id": task.bidder.merchant_account_id,
        	"amount": amount,
        	"credit_card": {
            	"number": credit_card.cleaned_data.get("card_number"),
            	"cvv": credit_card.cleaned_data.get("cvv"),
            	"expiration_month": credit_card.cleaned_data.get("expiration_month"),
            	"expiration_year": credit_card.cleaned_data.get("expiration_year"),
        		#"billing_address": {
        		#	"first_name": credit_card.cleaned_data.get("first_name"),
        		#	"last_name": credit_card.cleaned_data.get("last_name"),
				#	"street_address": credit_card.cleaned_data.get('street_address'),
				#	"extended_address": '',
				#	"locality": credit_card.cleaned_data.get('city'),
				#	"region": credit_card.cleaned_data.get('state'),
				#	"postal_code": credit_card.cleaned_data.get('zip_code'),
				#	"country_code_alpha2": 'US'
        		#}

        	},
        	"service_fee" : service_fee,
        	"options": {
            	"submit_for_settlement": True
        	}
    	})
    	
		if result.is_success:
			messages.success(request, ("success! Transaction ID: {0}").format(result.transaction.id))
			return HttpResponseRedirect(reverse('home'))
		else:
			messages.error(request, ("Error: {0}").format(result.message))
			return HttpResponseRedirect(reverse('home'))
