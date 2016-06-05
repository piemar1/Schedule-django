# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'

from django.db import models
from user_account.models import User


months = (
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

years = (
    ('2016', '2016'),
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


class Schedule(models.Model):

    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=200, unique=True, null=False)
    crew = models.OneToOneField(Team)
    year = models.CharField(max_length=20, choices=years)
    month = models.CharField(max_length=20, choices=months)
    schedule = models.TextField(null=True)
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return 'Schedule {}'.format(self.name)


class Person(models.Model):
    name = models.CharField(max_length=200, null=False)
    crew = models.ForeignKey(Team, null=True)

    def __str__(self):
        return 'Person {}'.format(self.name)


def get_teams_from_db():
    """ Zwraca listę z obiektami Team. """
    return [team for team in Team.objects.all()]


def get_team_from_db(team_name):
    """ Zwraca obiekt Team gdzie name=team_name."""
    team = Team.objects.get(name=team_name)
    return team


def remove_team(team_name):
    """ Usywa z bazy danych obiekt Team  gdzie  name=team_name."""
    team = Team.objects.get(name=team_name)
    team.delete()


def save_team_to_db(team_name, crew):
    """
    Zapisuje team do bazy, Jako arg przyjmuje instancję Team.
    Jeżeli dany wpis w db już istnieje, usuwa poprzedni wpis i tworzy nowy.
    """
    a_team = Team(name=team_name)
    a_team.save()
    print("Dokonano ZApisu TEAM", a_team.name)

    person_list = [Person(name=name) for name in crew]
    for person in person_list:
        person.crew = a_team
        person.save()
        print("Dokonano ZApisu Person", person.name)


def get_schedule_names_from_db():
    """ Zwraca listę stringów z nazwami schedules. """
    return [schedule.name for schedule in Schedule.objects.all()]


def save_schedule_to_db(schedule):
    """
    Zapisuje schedule do bazy, jako arg przyjmuję gotową instancję Schedule
    Jeżeli dany wpis w db już istnieje, usuwa poprzedni wpis i tworzy nowy.
    """
    pass


def delete_schedule_in_db(schedule_name_to_delete):
    """
    Usuwa wpis dla podanego schedule z bazy danych.
    """
    pass


def get_schedule_from_db(schedule_name_to_read):
    """Zwraca instancję Schedule na podstawie danych z db, jako arg przyjmuje schedule_name."""
    pass
