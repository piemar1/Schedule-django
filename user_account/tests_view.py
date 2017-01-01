from django.test import Client
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import User


class ScheduleViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        c = Client()
        c.login(username='testuser', password='12345')

    def test_login_registration(self):
        response = self.client.get(reverse('user_account:register'))
        self.assertEqual(response.status_code, 200)

    def test_success_registration(self):
        response = self.client.get(reverse('user_account:success_created'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(reverse('user_account:logout'))
        self.assertEqual(response.status_code, 200)

    def test_user_activation(self):
        """TEST NIESPRAWNY"""
        pass
        # response = self.client.get(reverse('user_account:activation'))
        # self.assertEqual(response.status_code, 200)

    def test_home(self):
        "Do napisania"
        pass

    def test_user_edit(self):
        "Do napisania"
        pass
