
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

class User(AbstractBaseUser):

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True, null=False)
    register_date = models.DateTimeField(auto_now=False, auto_now_add=True)     # ???
    register_updated = models.DateTimeField(auto_now=True, auto_now_add=False)  # ???
    active = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=40, default='')
    akey_expires = models.DateTimeField(default=timezone.now() + datetime.timedelta(2))

    def __str__(self):
        return 'User {} {}'.format(self.name, self.surname)

    def is_activ(self):
        return self.active

    @property                # ?????
    def get_email(self):
        return self.email
