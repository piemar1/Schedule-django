from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from user_account.models import User


# from prototype.cf.models import Movie

# from  import User

# from production import models as production_models
# class Car(models.Model):
#     manufacturer = models.ForeignKey(production_models.Manufacturer)



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

class Team(models.Model):

    name = models.CharField(max_length=200, unique=True, null=False)
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, null=True)

    def __str__(self):
        return 'Team {}'.format(self.name)

    def get_team_names_from_db(self):
        pass



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

