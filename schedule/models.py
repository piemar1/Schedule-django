import calendar

from django.db import models

from user_account.models import User
from . import solid_data as sd


class Team(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)
    user = models.ForeignKey(User, null=True)

    def __str__(self):
        return 'Team {}'.format(self.name)


class Schedule(models.Model):
    """Schedule model"""
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=200, unique=True, null=False)
    year = models.CharField(max_length=20, choices=sd.years)
    month = models.CharField(max_length=20, choices=sd.months)
    crew = models.ForeignKey(Team, null=False)

    def __str__(self):
        return 'Schedule {}'.format(self.name)

    def get_month_calendar(self):
        """
        Funkcja zwraca listę zawierającą informację o
        dniach tygodnia w kolejnych dniach miesiąca.
        """
        n = sd.MONTHS.index(self.month) + 1
        week_day, day_no = calendar.monthrange(int(self.year), n)

        week_days = []
        for day in range(day_no):
            week_days.append(sd.WEEK_DAYS[week_day])
            week_day += 1
            if week_day == 7:
                week_day = 0

        month_calendar = list(zip(
            [elem + 1 for elem in range(day_no)], week_days)
        )
        return month_calendar


class Person(models.Model):
    """Person model"""
    name = models.CharField(max_length=200, null=False)
    crew = models.ForeignKey(Team, null=True)

    def __str__(self):
        return 'Person {}'.format(self.name)


class OneSchedule(models.Model):
    """OneSchedule model"""
    schedule = models.ForeignKey(Schedule, null=True)
    one_schedule = models.TextField(max_length=50, null=True)
    person = models.ForeignKey(Person, null=True)

    def __str__(self):
        return 'OneSchedule for person {}'.format(self.person)

    def get_working_days_number_person(self):
        """
        Funkcja zwraca liczbę dyżurów dziennych lub
        nocnych w ciągu miesiąca grafiku.
        """
        return (
            self.one_schedule.count(sd.NIGHT) + self.one_schedule.count(sd.DAY)
        )

    def get_number_of_nights(self):
        """
        Funkcja zwraca liczbę dyżurów nocnych w ciągu miesiąca grafiku.
        """
        return self.one_schedule.count(sd.NIGHT)

    def wheather_day_is_free(self, number):
        """
        Metoda zwraca True jeśli osoba może przyjąć dyżur,
        False jeśli nie może przyjąć dyżuru. OK
        """
        return self.one_schedule[number] == sd.FREE_DAY

    def get_number_of_days(self):
        """
        Funkcja zwraca liczbę dyżurów dziennych w ciągu miesiąca grafiku.
        """
        return self.one_schedule.count(sd.DAY)

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

    def filtre_work_days_in_month(self, no_of_working_days):
        """
        Metoda zwraca True jeśli osoba ma mniej lyb tyle samo dni roboczych
        w miesiącu niż no_of_working_days, inaczej False.
        """
        return self.get_working_days_number_person() <= no_of_working_days

    def filtre_double_work(self, day_number, work):
        """
        Metoda zwraca False jeśli dodanie dyżuru
        spowoduje powstanie dyżuri 24 h ND, inaczej True
        """
        if day_number == 0 \
           and work == sd.NIGHT \
           and self.one_schedule[day_number + 1] == sd.DAY:
            return False

        elif 0 < day_number < len(self.one_schedule)-1:
            if work == sd.NIGHT and self.one_schedule[day_number+1] == sd.DAY:
                return False

            elif work == sd.DAY \
                    and self.one_schedule[day_number-1] == sd.NIGHT:
                return False

        elif day_number == len(self.one_schedule) - 1:
            if work == sd.DAY and self.one_schedule[day_number-1] == sd.NIGHT:
                return False
        return True

    def filtre_work_days_in_week(self, no_of_working_days, day_number):
        """
        Metoda zwraca True jeśli liczba dni roboczych w one_schedule
        w tygodniu nie przekracza no_of_working_days, inaczej False.
        """
        schedule_part = self.one_schedule[:day_number] \
            if day_number <= 6 \
            else self.one_schedule[day_number - 7: day_number]

        return schedule_part.count(sd.NIGHT) + \
            schedule_part.count(sd.DAY) < no_of_working_days
