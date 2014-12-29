from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from tasks.models import Task, Bid
from users.models import User

import braintree

# Create your tests here.
class CheckoutTest(TestCase):
    
    def setUp(self):
        self.worker = User.objects.create_superuser(
                email = 'worker@case.edu',
                first_name = 'John',
                last_name = 'Worker',
                password = 'password')
        self.worker.merchant_account_id='6pky6k4wn8zv8qv5'
        self.worker.save()

        self.studier = User.objects.create_superuser(
                email = 'studier@case.edu',
                first_name = 'John',
                last_name = 'Studier',
                password = 'password')
        
        self.task = Task.objects.create(
                title = 'Life',
                discription = 'love it',
                creator = self.studier,
                suggested_price=4.20)

        self.bid = Bid.objects.create(
                bid = 4.19,
                message = 'Perfect price',
                bidder = self.worker,
                task = self.task)
        self.task.accept_bid(self.bid)

    def test_checkout_view(self):
        studier = User.objects.get(pk='studier@case.edu')
        task = Task.objects.get(pk=1)
        print task.title
        """
        self.assertEqual(studier.email, 'studier@case.edu')
        c = Client()
        c.login(email=self.studier.email, password='password')
        resp = c.post(reverse('checkout:checkout', kwargs={'pk':self.task.pk}),
                {'card_number': '5555555555554444',
                 'cvv': '111',
                 'expiration_month': '05',
                 'expiration_year' : '20',
                 })
        self.assertNotEqual(resp.status_code,403)
        """
        BRAINTREE_MERCHANT_ID = "6pky6k4wn8zv8qv5"

        BRAINTREE_PUBLIC_KEY = "wjnjmcvgks67jqwj"

        BRAINTREE_PRIVATE_KEY = "0644195d268ff95465a555bf2647655b"

        braintree.Configuration.configure(
            braintree.Environment.Sandbox,
            BRAINTREE_MERCHANT_ID,
            BRAINTREE_PUBLIC_KEY,
            BRAINTREE_PRIVATE_KEY
        )


        amount = 4.19
        service_fee = amount * 0.2
        worker_fee = amount - service_fee


        result = braintree.Transaction.sale({
            "amount": str(amount),
            "credit_card": {
                "number": "4111111111111111",
                "cvv": "111",
                "expiration_month": "05",
                "expiration_year": "2020",
                #"billing_address": {
                #   "first_name": credit_card.cleaned_data.get("first_name"),
                #   "last_name": credit_card.cleaned_data.get("last_name"),
                #   "street_address": credit_card.cleaned_data.get('street_address'),
                #   "extended_address": '',
                #   "locality": credit_card.cleaned_data.get('city'),
                #   "region": credit_card.cleaned_data.get('state'),
                #   "postal_code": credit_card.cleaned_data.get('zip_code'),
                #   "country_code_alpha2": 'US'
                #}

            }
        })
        
        
        self.assertTrue(result.is_success)
