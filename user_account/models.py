from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True, null=False)
    register_date = models.DateTimeField(auto_now=False, auto_now_add=True)    # ????
    register_updated = models.DateTimeField(auto_now=True, auto_now_add=False)   # ????
    active = models.BooleanField(default=False)

    def __str__(self):
        return 'User {} {}'.format(self.name, self.surname)

    def is_activ(self):
        return self.active

    def get_email(self):
        return self.email
