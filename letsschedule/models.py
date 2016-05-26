
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


MONTHS = (
    (u"styczeń", u"styczeń"),
    (u"luty", u"luty"),
    (u"marzec", u"marzec"),
    (u"kwiecień", u"kwiecień"),
    (u"maj", u"maj"),
    (u"czerwiec", u"czerwiec"),
    (u"lipiec", u"lipiec"),
    (u"sierpień", u"sierpień"),
    (u"wrzesień", u"wrzesień"),
    (u"październik", u"październik"),
    (u"listopad", u"listopad"),
    (u"grudzień", u"grudzień")
)

YEARS = (
    ('2016','2016'),
    ('2017', '2017'),
    ('2018', '2018'),
    ('2019', '2019'),
    ('2020', '2020')
)


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


class Team(models.Model):

    name = models.CharField(max_length=200, unique=True, null=False)
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, null=True)

    def __str__(self):
        return 'Team {}'.format(self.name)


class Schedule(models.Model):

    name = models.CharField(max_length=200, unique=True, null=False)
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    crew = models.OneToOneField(Team)
    month = models.CharField(max_length=20, choices=MONTHS)
    year = models.CharField(max_length=20, choices=YEARS)
    schedule = models.TextField(null=True)
    user = models.ForeignKey(User, null=True)


    def __str__(self):
        return 'Schedule {}'.format(self.name)


class Person(models.Model):

    name = models.CharField(max_length=200, null=False)
    surname = models.CharField(max_length=200, null=False)
    crew = models.ForeignKey(Team, null=True)



    def __str__(self):
        return 'Person {} {}'.format(self.name, self.surname)









