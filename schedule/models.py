# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'

# kolejność importów: najpierw libki Pythonowe, zainstalowane biblioteki, na końcu importy lokalne
import calendar

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

MONTHS = [
    u"styczeń", u"luty", u"marzec", u"kwiecień", u"maj", u"czerwiec", u"lipiec",
    u"sierpień", u"wrzesień", u"październik", u"listopad", u"grudzień"
]
# MONTHS = [m[0] for m in months] żeby nie duplikować?

WEEK_DAYS = {
    0: u"pn", 1: u"wt", 2: u"śr", 3: u"cz", 4: u"pt", 5: u"so", 6: u"n"
}


class Team(models.Model):

    name = models.CharField(max_length=200, unique=True, null=False)
    user = models.ForeignKey(User, null=True)

    def __str__(self):
        return 'Team {}'.format(self.name)


class Schedule(models.Model):
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=200, unique=True, null=False)
    year = models.CharField(max_length=20, choices=years)
    month = models.CharField(max_length=20, choices=months)
    crew = models.ForeignKey(Team, null=False)

    def __str__(self):
        return 'Schedule {}'.format(self.name)

    def get_month_calendar(self):

        # import pdb; pdb.set_trace()

        n = MONTHS.index(self.month) + 1
        week_day, day_no = calendar.monthrange(int(self.year), n)

        week_days = []
        for day in range(day_no):
            week_days.append(WEEK_DAYS[week_day])
            week_day += 1
            if week_day == 7:
                week_day = 0

        month_calendar = list(zip([elem + 1 for elem in range(day_no)], week_days))
        # print("month_calendar", month_calendar)

        return month_calendar


class Person(models.Model):
    name = models.CharField(max_length=200, null=False)
    crew = models.ForeignKey(Team, null=True)

    def __str__(self):
        return 'Person {}'.format(self.name)


class OneSchedule(models.Model):
    schedule = models.ForeignKey(Schedule, null=True)
    one_schedule = models.TextField(max_length=50, null=True)
    person = models.ForeignKey(Person, null=True)

    def __str__(self):
        return 'OneSchedule for person {}'.format(self.person)


    def get_working_days_number_person(self):
        """
        Funkcja zwraca liczbę dyżurów dziennych lub nocnych w ciągu miesiąca grafiku.
        """
        number = 0
        for day in self.one_schedule:
            if day in u"DN":
                number += 1
        return number


    def get_number_of_nights(self):
        """
        Funkcja zwraca liczbę dyżurów nocnych w ciągu miesiąca grafiku.
        """
        number = 0
        for day in self.one_schedule:
            if day in u"N":
                number += 1
        return number


    def get_number_of_days(self):
        """
        Funkcja zwraca liczbę dyżurów dziennych w ciągu miesiąca grafiku.
        """
        number = 0
        for day in self.one_schedule:
            if day in u"D":
                number += 1
        return number

    def take_work(self, day_number, work):
        """
        Metoda wprowadza zmiany w grafiku dla danego dnia i rodzaju dyżuru.
        """
        if day_number == 0:
            self.one_schedule = "{}{}".format(work, self.one_schedule[1:])
        else:
            self.one_schedule = "{}{}{}".format(
                self.one_schedule[:day_number],
                work,
                self.one_schedule[day_number + 1:]
            )


###########################################

############################################3



# def get_teams_from_db():
#     """ Zwraca listę z obiektami Team. """
#     return Team.objects.all()


# def get_team_from_db(team_name):
#     """ Zwraca obiekt Team gdzie name=team_name."""
#     # po wrzuceniu do widokw moze przyda sie https://docs.djangoproject.com/en/1.9/topics/http/shortcuts/#get-object-or-404
#     return Team.objects.get(name=team_name)


# def get_schedule_from_db(schedule_name):
#     """Zwraca instancję Schedule na podstawie danych z db, jako arg przyjmuje schedule_name."""
#     return Schedule.objects.get(name=schedule_name)


# def remove_team(team_name):
#     """ Usywa z bazy danych obiekt Team  gdzie  name=team_name."""
#     team = Team.objects.get(name=team_name)
#     team.delete()


# def remove_schedule(schedule_name):
#     """ Usuwa wpis dla podanego schedule z bazy danych. """
#     schedule = Schedule.objects.get(name=schedule_name)
#     schedule.delete()


# def save_team_to_db(team_name, crew):
#     """
#     Zapisuje team do bazy, Jako arg przyjmuje instancję Team.
#     Jeżeli dany wpis w db już istnieje, usuwa poprzedni wpis i tworzy nowy.
#     """
#     a_team = Team(name=team_name)
#     a_team.save()
#
#     person_list = [Person(name=name) for name in crew]
#     for person in person_list:
#         person.crew = a_team
#         person.save()


# def get_schedule_names_from_db():
#     """ Zwraca listę stringów z nazwami schedules. """
#     return [schedule.name for schedule in Schedule.objects.all()]





