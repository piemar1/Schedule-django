# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'

from .solid_data import *


def get_number_of_free_worktype(day_number, one_schedules, work):
    """
    Zwraca liczbę osób z obsadzonymi dyżurami dla danego dnia i rodzaju dyżuru
    """
    number = 0
    for one_schedule in one_schedules:
        if one_schedule.one_schedule[day_number] == work:
            number += 1
    return number


def get_free_people(day_number, one_schedules, work, no_of_working_days):
    """
    Zwraca listę osób (w postaci atrybutów person.name),
    które moga przyjąć dyżur -
    Tutaj muszą być wszystkie filtry
    - osoba bez dyżuru
    - 2 dyżury pod rząd, 24h
    - liczba dyżurów w tygodniu
    - liczba dyżurów w miesiącu
    """

    # Właściwa selekcja osób którym można przydzielić dany dyżur w danym dniu
    selected_person = [
        one_schedule for one_schedule in one_schedules if
        one_schedule.wheather_day_is_free(day_number) and
        one_schedule.filtre_double_work(day_number, work) and
        one_schedule.filtre_work_days_in_week(4, day_number) and
        one_schedule.filtre_work_days_in_month(no_of_working_days)
        ]

    # porządkowanie lisry osób ze względeu na liczbą przydzielonych dyżurów
    selected_person.sort(
        key=lambda one_schedule: one_schedule.get_working_days_number_person(),
        reverse=True
    )

    return [one_schedule.person.name for one_schedule in selected_person]


def get_position_of_person(person_name, one_schedules):
    for number, one_schedule in enumerate(one_schedules):
        if one_schedule.person.name == person_name:
            return number
    return


def fill_the_schedule(one_schedules, no_of_working_days,
                      person_per_day, person_per_night):

    month_lenght = len(one_schedules[0].one_schedule)

    for day_number in range(month_lenght):

        # NIGHTS
        # liczba osób potrzebnych
        number_of_need_night = person_per_night - get_number_of_free_worktype(
            day_number, one_schedules, NIGHT
        )

        # tworzenie listy ludzi którzy mogą przyjąć dyżur
        list_of_free_persons = get_free_people(
            day_number,
            one_schedules,
            NIGHT,
            no_of_working_days
        )

        for night in range(number_of_need_night):
            # wybór osoby
            selected_person_name = list_of_free_persons.pop()

            # zdobycie numeru wylosowanej osoby w liście people
            selected_person_number = get_position_of_person(
                selected_person_name, one_schedules
            )

            # wprowadzenie zmiany do grafiku
            one_schedules[selected_person_number].take_work(day_number, NIGHT)

        # DAYS
        # liczba osób potrzebnych
        number_of_need_days = person_per_day - get_number_of_free_worktype(
            day_number, one_schedules, DAY
        )

        # tworzenie listy ludzi którzy mogą przyjąć dyżur
        list_of_free_persons = get_free_people(
            day_number, one_schedules, DAY, no_of_working_days
        )

        for day in range(number_of_need_days):
            # wybór osoby
            selected_person_name = list_of_free_persons.pop()

            # zdobycie numeru wylosowanej osoby w liście people
            selected_person_number = get_position_of_person(
                selected_person_name, one_schedules
            )

            # wprowadzenie zmiany do grafiku
            one_schedules[selected_person_number].take_work(day_number, DAY)

    return one_schedules
