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
        self.worker = User.objects.create_superuser(
            email='life@me.co',
            first_name='John',
            last_name='Worker',
            password='password',
            )
        
        self.studier = User.objects.create_superuser(
            email='adc82@cim.edu',
            first_name='John',
            last_name='Studier',
            password='password')

        self.bidder = User.objects.create_superuser(
            email='adc82@cia.edu',
            first_name='John',
            last_name='bidder',
            password='password')
        
        self.user = User.objects.create_superuser(
            email='adc82@cwru.edu',
            first_name='John',
            last_name='Doe',
            password='password')
        
        self.task = Task.objects.create(
               title='love',
               discription='life',
               suggested_price=4.20,
               creator=User.objects.get(pk='adc82@cim.edu'))

        self.bid = Bid.objects.create(
               bid=3.33,
               bidder=User.objects.get(pk='life@me.co'),
               message="Am I just eating because I'm bord",
               task=Task.objects.get(pk=1))

        self.bid2 = Bid.objects.create(
               bid=3.00,
               bidder=User.objects.get(pk='adc82@cwru.edu'),
               message="Am I just eating because I'm bord",
               task=Task.objects.get(pk=1))

    def test_accept_bid_method(self):
        task = Task.objects.get(pk=1)
        bid = Bid.objects.get(pk=1)
        bidder = User.objects.get(pk='life@me.co')
        #Test to make sure everything is set up properly        
        self.assertNotEqual(task.worker,bidder)
        self.assertNotEqual(task.accepted_bid, bid)
        self.assertFalse(task.accepted)
        
        task.accept_bid(bid)

        task = Task.objects.get(pk=1)
        bid = Bid.objects.get(pk=1)
        bidder = User.objects.get(pk='life@me.co')
        #test to make sure the proper changes were made
        self.assertEqual(task.worker, bidder)
        self.assertEqual(task.accepted_bid, bid)
        self.assertTrue(task.accepted)
        
        bad_bid = Bid.objects.get(pk=2)
        passed = False
        #test to make sure an error is raised if task has already been accepted
        try:
            self.assertRaises(task.accept_bid(bad_bid), ValidationError)
        except ValidationError:
            passed = True
        self.assertTrue(passed)
        
    def test_create_review_view(self):
        task = Task.objects.get(pk=1)
        bid = Bid.objects.get(pk=1)
        task.accept_bid(bid)
        #Test to make sure review of creator is none before adding it
        task = Task.objects.get(pk=1)
        self.assertIsNone(task.review_of_creator)
        c = Client()
        c.login(email='life@me.co', password='password')
        resp = c.post(reverse('tasks:create_review', kwargs={'task_pk':1}), 
                {'rating':10, 'comments':'great personality'})
        #Test to make sure the review is added to the review_of_creator 
        self.assertEqual(resp.status_code, 302)
        task = Task.objects.get(pk=1)
        self.assertIsNotNone(task.review_of_creator)
        #test to make sure review_of_worker is added
        task = Task.objects.get(pk=1)
        self.assertIsNone(task.review_of_worker)
        c.login(email='adc82@cim.edu', password='password')
        resp = c.post(reverse('tasks:create_review', kwargs={'task_pk':1}), 
                {'rating':10, 'comments':'great personality'})
        #Test to make sure review of worker is none before adding it
        self.assertEqual(resp.status_code, 302)
        task = Task.objects.get(pk=1)
        self.assertIsNotNone(task.review_of_worker)
        #Make sure that the review doesn't change when the wrong user logs in        
        c.login(email='adc82@cwru.edu', password='password')
        resp = c.post(reverse('tasks:create_review', kwargs={'task_pk':1}), 
                {'rating':10, 'comments':'great personality'})

        updated_task = Task.objects.get(pk=1)
        self.assertEqual(task.review_of_creator, updated_task.review_of_creator)
        self.assertEqual(task.review_of_worker, updated_task.review_of_worker)

    def test_accept_a_bid_view(self):
        #Test to make sure you have to be login to access view
        c = Client()
        resp = c.get(reverse('tasks:accept_bid', 
            kwargs={'task_pk':self.task.pk, 'bid_pk':self.bid.pk}
            ))
        task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(task.accepted)
        self.assertIsNone(task.worker)
        self.assertIsNone(task.accepted_bid)
        #Test to check if the wrong  user is login gets a 302 status code       
        c.logout()
        c.login(email=self.worker.email, password='password')
        resp = c.get(reverse('tasks:accept_bid', 
            kwargs={'task_pk':self.task.pk, 'bid_pk':self.bid.pk}
            ))
        
        task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(task.accepted)
        self.assertIsNone(task.worker)
        self.assertIsNone(task.accepted_bid)
        c.logout()
        #Tests to see if a bid is properly accepted
        c.login(email=self.studier.email, password='password')
        resp = c.get(reverse('tasks:accept_bid', 
            kwargs={'task_pk':self.task.pk, 'bid_pk':self.bid.pk}
            ))
        task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(task.accepted)
        self.assertEqual(task.worker, self.worker)
        self.assertEqual(task.accepted_bid, self.bid)

        c = Client()
        self.user.is_worker = False
        self.user.save()

    def test_accept_task_view(self):
        task = Task.objects.get(pk=self.task.pk)
        self.assertIsNone(task.accepted_bid)
        #test to make sure task is  by worker
        c = Client()
        c.login(email=self.worker.email, password='password')
        resp = c.get(reverse('tasks:accept_task', 
            kwargs={'pk':self.task.pk}))
        task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(resp.status_code, 302)
        self.assertIsNotNone(task.accepted_bid)


    def test_create_bid_view(self):
        c = Client()
        self.user.is_worker = False
        self.user.save()
        c.login(email=self.user.email, password='password')
        resp = c.get(reverse('tasks:create_bid', kwargs={'pk':self.task.pk}))
        #Test to make sure PermissionDenied is raised for a user that isn't
        #a worker
        self.assertEqual(resp.status_code, 403)
        
        c.login(email=self.worker.email, password='password')
        resp = c.get(reverse('tasks:create_bid', kwargs={'pk':self.task.pk}))
        #Test to make sure PermissionDenied is not raised
        self.assertEqual(resp.status_code, 200)
       
        c.login(email=self.user.email, password='password')
        resp = c.post(reverse('tasks:create_bid', kwargs={'pk':self.task.pk}),
                {'bid':2.00, 'message':'I love cake'})
        

        self.assertEqual(resp.status_code, 403)
        c.login(email=self.worker.email, password='password')
        resp = c.post(reverse('tasks:create_bid', kwargs={'pk':self.task.pk}),
                {'bid':2.00, 'message':'I love cake'})
        
        self.assertEqual(resp.status_code, 302)
        bid = Bid.objects.get(bid=2.00)
        self.assertIsNotNone(bid)

    def test_complete_task_view(self):
        pass
    
    def test_create_review_view(self):
        task = Task.objects.get(pk=self.task.pk)
        task.accept_bid(self.bid)
        
        c = Client()
        c.login(email=self.user.email, password='password')
        resp = c.post(reverse('tasks:create_review', kwargs={'task_pk':self.task.pk}),
                {'comments':'Thaks for the help','rating':9})
        #Test to make sure permission denied is raised
        self.assertEqual(resp.status_code, 403)       

        #Test to make sure review of creator is porperly created
        task = Task.objects.get(pk=self.task.pk)
        self.assertIsNone(task.review_of_creator)
        c.login(email=self.worker.email, password='password')
        resp = c.post(reverse('tasks:create_review', kwargs={'task_pk':self.task.pk}),
                {'comments':'Thaks for the help','rating':9})
        task = Task.objects.get(pk=self.task.pk)
        self.assertIsNotNone(task.review_of_creator)
        self.assertEqual(resp.status_code, 302)
        
        #Test to make sure review of worker is properly created
        self.assertIsNone(task.review_of_worker)
        c.login(email=self.studier.email, password='password')
        resp = c.post(reverse('tasks:create_review', kwargs={'task_pk':self.task.pk}),
                {'comments':'Thaks for the help','rating':9})
        task = Task.objects.get(pk=self.task.pk)
        self.assertIsNotNone(task.review_of_worker)
        self.assertEqual(resp.status_code, 302)

    def test_create_task_view(self):
        c = Client()
        resp = c.get(reverse('tasks:create_task'))
        self.assertEqual(resp.status_code, 302)

        c.login(email=self.studier, password='password')
        resp = c.get(reverse('tasks:create_task'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('tasks/createTask.html')

        resp = c.post(reverse('tasks:create_task'),
                {'title':'someone play tennis with me',
                 'discription': 'anyone......',
                 'suggested_price': .01})

        task = Task.objects.get(title='someone play tennis with me')
        self.assertIsNotNone(task)


    def test_test_detail_view(self):
        c = Client()
        self.user.is_worker = False
        self.user.save()
        c = Client() 
        resp = c.get(reverse('tasks:task', 
            kwargs={'pk':1}), follow=True)
        self.assertTrue(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'tasks/taskDetail.html')
        
        c.login(email=self.worker, password='password')
        resp = c.get(reverse('tasks:task', 
            kwargs={'pk':1}), follow=True)
        self.assertTrue(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'tasks/taskDetailWorker.html')
        self.client.logout()
        
        c.login(email=self.studier.email, password='password')
        resp = c.get(reverse('tasks:task', 
            kwargs={'pk':1}), follow=True)
        self.assertTrue(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'tasks/taskDetailCreator.html')

    def test_task_list_view(self):
        c = Client()
        resp = c.get(reverse('tasks:task_list'))
        self.assertTrue(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'tasks/taskList.html')
