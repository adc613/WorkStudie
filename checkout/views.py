from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied 
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

import stripe

from forms import CreditCardInfo
from tasks.models import Task

from django.views.generic.base import TemplateView

class t(TemplateView):
    template_name='t.html'

class CheckoutView(View):
    """
    Will checkout user and add the correct amount of money
    to their wallets.
    """
    template_name = "checkout/checkout.html"
    credit_card_form = CreditCardInfo
    def get(self, request, **kwargs):
        """
        task = Task.objects.get(pk=kwargs['pk'])
        if not request.user == task.creator:
            raise PermissionDenied("You're not allowed to pay for this")
        return render(request, self.template_name, 
            {'form' : self.credit_card_form})
        """
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        stripe.api_key = "sk_test_nTicxpM9LwG9jtWYYhKrLvA7"
        life = request.POST.get('life', '') 
        card = request.POST.get('stripeToken', '')
        
        stripe.Charge.create(
            amount= 10000,
            currency="USD",
            card=card,
            description="Test charge")

        return HttpResponseRedirect(reverse('home'))
        

        """
        task = Task.objects.get(pk=1)
        email = request.user.email
        if request.user != task.creator:
            raise PermissionDenied("You're not allowed to pay for this")
        credit_card = self.credit_card_form(request.POST or None)
        #if not (credit_card.is_valid()):
         #   message.error(request, "credit card form is not valid")
          #  return HttpResponseRedirect(reverse('home')) #redirect to the same page later
        
        amount = task.accepted_bid.bid
        service_fee = amount * .2
        worker_fee = amount - service_fee
        """
        
