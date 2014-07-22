from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client

from .models import *
from users.models import User

# Create your tests here.
class TasksViewsTest(TestCase):

	fixtures=['fixture02.json']
	worker = User.objects.get(email='adc82@cim.edu')
	studier = User.objects.get(email='adc95@comcast.net')
	super_user = User.objects.get(email='adc82@case.edu')
	task = Task.objects.get(pk=1)
	bid = Bid.objects.get(pk=1)
	def setUp(self):
		# Every test needs a client.
		self.client = Client()

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


