import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.core.exceptions import ValidationError

from .models import *
from users.models import User

# Create your tests here.
class TasksViewsTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(
            email='life@me.co',
            first_name='John',
            last_name='Worker',
            password='password',
            )
        
        User.objects.create_superuser(
            email='adc82@cim.edu',
            first_name='John',
            last_name='Studier',
            password='password')

        User.objects.create_superuser(
            email='adc82@cia.edu',
            first_name='John',
            last_name='bidder',
            password='password')
        
        User.objects.create_superuser(
            email='adc82@cwru.edu',
            first_name='John',
            last_name='Doe',
            password='password')

        Task.objects.create(
               title='love',
               discription='life',
               suggested_price=4.20,
               creator=User.objects.get(pk='adc82@cim.edu'))

        Bid.objects.create(
               bid=3.33,
               bidder=User.objects.get(pk='life@me.co'),
               message="Am I just eating because I'm bord",
               task=Task.objects.get(pk=1))

        Bid.objects.create(
               bid=3.00,
               bidder=User.objects.get(pk='adc82@cwru.edu'),
               message="Am I just eating because I'm bord",
               task=Task.objects.get(pk=1))

    def test_accept_bid_method(self):
        task = Task.objects.get(pk=1)
        bid = Bid.objects.get(pk=1)
        bidder = User.objects.get(pk='life@me.co')
        
        self.assertNotEqual(task.worker,bidder)
        self.assertNotEqual(task.accepted_bid, bid)
        self.assertFalse(task.accepted)
        
        task.accept_bid(bid)

        task = Task.objects.get(pk=1)
        bid = Bid.objects.get(pk=1)
        bidder = User.objects.get(pk='life@me.co')
        
        self.assertEqual(task.worker, bidder)
        self.assertEqual(task.accepted_bid, bid)
        self.assertTrue(task.accepted)

        bad_bid = Bid.objects.get(pk=2)
        passed = False
        try:
            self.assertRaises(task.accept_bid(bad_bid), ValidationError)
        except ValidationError:
            passed = True

        self.assertTrue(passed)
        
    def test_complete_bid_method

        

"""
	def test_accept_a_bid_view(self):
		#Test to make sure you have to be login to access view
		resp = self.client.get(reverse('task:accept_bid', 
			kwargs={'task_pk':self.task.pk, 'bid_pk':self.bid.pk}
			))
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp.status_code, 302)
		self.assertFalse(self.task.accepted)
		self.assertEqual(self.task.worker, None)
		self.assertEqual(self.task.accepted_bid, None)
		#Test to check if a user login gets a 200 status code		
		self.client.logout()
		self.client.login(email='adc82@cim.edu', password='ramrod')
		resp = self.client.get(reverse('task:accept_bid', 
			kwargs={'task_pk':self.task.pk, 'bid_pk':self.bid.pk}
			))
		
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp.status_code, 302)
		self.assertFalse(self.task.accepted)
		self.assertEqual(self.task.worker, None)
		self.assertEqual(self.task.accepted_bid, None)
		self.client.logout()
		#Tests to see if a bid is properly accepted
		self.client.login(email='adc95@comcast.net', password='ramrod')
		resp = self.client.get(reverse('task:accept_bid', 
			kwargs={'task_pk':self.task.pk, 'bid_pk':self.bid.pk}
			))
		self.assertEqual(resp.status_code, 302)
		self.assertTrue(self.task.accepted)
		self.assertEqual(self.task.worker, self.worker)
		self.assertEqual(self.task.accepted_bid, self.bid)
		self.client.logout()

	def test_accept_task_view(self):
		self.client.login(email='adc82@case.edu', password='ramrod')
		resp = self.client.get(reverse('task:accept_task', 
			kwargs={'pk':self.task.pk}))
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(self.task.accepted_bid,
			Bid.objects.get(pk=2))

	def test_create_bid_view(self):
		pass

	def test_complete_task_view(self):
		pass

	def test_create_review_view(self):
		pass

	def test_create_task_view(self):
		self.client.login(email='adc95@comcast.net', password='ramrod')
		resp = self.client.get(reverse('task:create_task'))
		self.assertEqual(resp.status_code, 302)
		self.assertTemplateUsed('createTask.html')
		self.client.logout()
		resp = self.client.get(reverse('task:create_task'))
		self.assertEqual(resp.status_code, 302)



	def test_test_detail_view(self):
		self.client.logout()
		resp = self.client.get(reverse('task:task', 
			kwargs={'pk':1}), follow=True)
		self.assertTrue(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'taskDetail.html')
		
		self.client.login(email='adc82@case.edu', password='ramrod')
		resp = self.client.get(reverse('task:task', 
			kwargs={'pk':1}), follow=True)
		self.assertTrue(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'taskDetailWorker.html')
		self.client.logout()
		
		self.client.login(email='adc95@comcast.net', password='ramrod')
		resp = self.client.get(reverse('task:task', 
			kwargs={'pk':1}), follow=True)
		self.assertTrue(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'taskDetailCreator.html')
		self.client.logout()

	def test_task_list_view(self):
		resp = self.client.get(reverse('task:task_list'))
		self.assertTrue(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'taskList.html')
		self.client.login(email='adc82@cim.edu', password='ramrod')
		resp = self.client.get(reverse('task:task_list'))
		self.client.login(email='adc95@comcast.net', password='ramrod')
		self.client.login(email='adc82@case.edu', password='ramrod')

"""
