from django.test import Client
from django.core.urlresolvers import reverse
from django.test import TestCase

from user_account.models import User


class ScheduleViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        c = Client()
        c.login(username='testuser', password='12345')

    def test_main_page(self):
        response = self.client.get(reverse('schedule:main_page'))
        self.assertEqual(response, reverse('user_account:register'))
