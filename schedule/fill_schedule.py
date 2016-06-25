# -*- coding: utf-8 -*-
__author__ = 'Marcin Pieczyński'


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
    Zwraca listę osób (w postaci atrybutów person.name), które moga przyjąć dyżur -
    Tutaj muszą być wszystkie filtry
    - osoba bez dyżuru
    - 2 dyżury pod rząd, 24h
    - liczba dyżurów w tygodniu
    - liczba dyżurów w miesiącu
    """

    # Właściwa selekcja osób którym można przydzielić dany dyżur w danym dniu
    selected_person = [one_schedule for one_schedule in one_schedules if
                       one_schedule.wheather_day_is_free(day_number) and
                       one_schedule.filtre_double_work(day_number, work) and
                       one_schedule.filtre_work_days_in_week(4, day_number) and
                       one_schedule.filtre_work_days_in_month(no_of_working_days)]

    # porządkowanie lisry osób ze względeu na liczbą przydzielonych dyżurów
    selected_person.sort(key=lambda one_schedule: one_schedule.get_working_days_number_person(), reverse=True)

    return [one_schedule.person.name for one_schedule in selected_person]


def get_position_of_person(person_name, one_schedules):
    for number, one_schedule in enumerate(one_schedules):
        if one_schedule.person.name == person_name:
            return number
    return


###################################################

def fill_the_schedule(one_schedules, no_of_working_days, person_per_day, person_per_night):

    month_lenght = len(one_schedules[0].one_schedule)
    # print(month_lenght)

    for day_number in range(month_lenght):
        # print("day_number", day_number +1)

        # NIGHTS

        # liczba osób potrzebnych
        number_of_need_night = person_per_night - get_number_of_free_worktype(day_number, one_schedules, "N")
        # print(number_of_need_night)

        # tworzenie listy ludzi którzy mogą przyjąć dyżur    Wszystkie FILTRY !!!!!!!
        list_of_free_persons = get_free_people(day_number, one_schedules, "N", no_of_working_days)
        # print("list_of_free_persons", list_of_free_persons)

        for night in range(number_of_need_night):
            # wybór osoby
            selected_person_name = list_of_free_persons.pop()

            # zdobycie numeru wylosowanej osoby w liście people
            selected_person_number = get_position_of_person(selected_person_name, one_schedules)
            # print("selected_person_number", one_schedules[selected_person_number].person.name)

            # wprowadzenie zmiany do grafiku
            one_schedules[selected_person_number].take_work(day_number, "N")

        # DAYS

        # liczba osób potrzebnych
        number_of_need_days = person_per_day - get_number_of_free_worktype(day_number, one_schedules, "D")
        # print(number_of_need_days)

        # tworzenie listy ludzi którzy mogą przyjąć dyżur    Wszystkie FILTRY !!!!!!!
        list_of_free_persons = get_free_people(day_number, one_schedules, "D", no_of_working_days)
        # print("list_of_free_persons", list_of_free_persons)

        for day in range(number_of_need_days):
            # wybór osoby
            selected_person_name = list_of_free_persons.pop()

            # zdobycie numeru wylosowanej osoby w liście people
            selected_person_number = get_position_of_person(selected_person_name, one_schedules)
            # print("selected_person_number", one_schedules[selected_person_number].person.name)

            # wprowadzenie zmiany do grafiku
            one_schedules[selected_person_number].take_work(day_number, "D")

        # for one_schedule in one_schedules:
        #     print(one_schedule.person.name[:3], one_schedule.one_schedule)

    return one_schedules





if __name__ == '__main__':

    work = (u"D", u"N", u"U", u".")

    person_per_day = 4       # liczba osón na dyżurze dziennym
    person_per_night = 2     # liczba osón na dyżurze nocnym
    number_of_working_days = 14


    crew = [u'A', u'B', u'C', u'D', u'E',
            u'F', u'G', u'H', u'I', u'J',
            u'K', u'L', u'M', u'N', u'O']

    small_schedules = [
        u'D.........UUUUUU..............N',
        u'.D...........................N.',
        u'..D.........................N..',
        u'...D.................UUUUUUN...',
        u'....D.....................N....',
        u'.....D...................N.....',
        u'......D.................N......',
        u'.......D...............N.......',
        u'........D.............N........',
        u'UUU...UUUUUUU........N.........',
        u'..........D.........N..........',
        u'...........D..UUUUUUUU.........',
        u'............D.....N............',
        u'.............D...N.............',
        u'..............D.N..............'
    ]

    from django.db import models


    # klasa stworzona tylko w telach testowych modułu
    class OneSchedule:
        def __init__(self, person, small_schedule):
            self.person = person
            self.one_schedule = small_schedule

    one_schedules = [OneSchedule(person, small_schedule)
                     for person, small_schedule in zip(crew, small_schedules)]

    fill_the_schedule(one_schedules, number_of_working_days, person_per_day, person_per_night)

    # for no,(name, one_schedule) in enumerate(zip(first_schedule.crew, first_schedule.schedule)):
    #     person = Person(name, one_schedule)
    #
    #     print(name, one_schedule, person.get_number_of_nights(),
    #           person.get_number_of_days(), person.get_working_days_number_person())