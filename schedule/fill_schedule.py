# -*- coding: utf-8 -*-
__author__ = 'Marcin Pieczyński'


# import random


# def create_team_for_schedule_filing(schedule):
#     """
#     Tworzy instancje klas Person w celu uzupełniania grafiku
#     """
#     crew = schedule.crew
#     schedules = schedule.schedule
#     return [Person(name, person_schedule) for name, person_schedule in zip(crew, schedules)]

class PersonSchedule:
    def __init__(self, name, schedule):
        self.name = name
        self.schedule = schedule

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_working_days_number_person(self):
        """
        Funkcja zwraca liczbę dyżurów dziennych lub nocnych w ciągu miesiąca grafiku.
        ##########################################################################
        TAKA SAMA METHODA JEST W CLASIE ONESCHEDULE !!!!!!!!!!!!!!!!!!!!!!!!!
        ##########################################################################
        """
        number = 0
        for day in self.schedule:
            if day in u"DN":
                number += 1
        return number

    def wheather_day_is_free(self, number):
        """
        Metoda zwraca True jeśli osoba może przyjąć dyżur, False jeśli nie może przyjąć dyżuru. OK
        """
        if self.schedule[number] == ".":
            return True
        return False

    def take_work(self, day_number, work):
        """
        Metoda wprowadza zmiany w grafiku dla danego dnia i rodzaju dyżuru.
        Identyczna metoda jest w clasie ONESCHEDULE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        """
        if day_number == 0:
            self.schedule = "{}{}".format(work, self.schedule[1:])
        else:
            self.schedule = "{}{}{}".format(
                self.schedule[:day_number],
                work,
                self.schedule[day_number + 1:]
            )

    @staticmethod
    def _filtr_working_days_in_week(string, working_days_number):
        """
        Funkcja zwraca True jeśli liczba dni roboczych w str nie przekracza 4, inaczej False
        """
        number = 0
        for day in string:
            if day in u"DN":
                number += 1
        if number > working_days_number:
            return False
        return True

    def filtre_double_work(self):
        """
        Metoda zwraca True jeśli osoba nie ma podwójnego dyżuru ND - nocka - dniówka 24h, inaczej False.
        """
        if "ND" in self.schedule:
            return False
        return True

    def filtre_work_days_in_week(self, working_days_number):
        """
        Metoda zwraca True jeśli liczba dni roboczych w schedule w tygodniu nie przekracza 4, inaczej False.
        """
        schedule_parts = [self.schedule[number:number + 7] for number in range(len(self.schedule) - 7)]
        result = all([self._filtr_working_days_in_week(parts, working_days_number) for parts in schedule_parts])

        return result
        # wersja stara !!!!
        # if results:
        #     return True
        # return False

    def filtre_work_days_in_month(self, no_of_working_days):
        """
        Metoda zwraca Trur jeśli osoba ma mniej dni roboczych w miesiącu niż no_of_working_days, inaczej False.
        """
        if self.get_working_days_number_person() <= no_of_working_days:
            return True
        return False

def get_number_of_free_worktype(day_number, one_schedules, work):
    """
    Zwraca liczbę osób z obsadzonymi dyżurami dla danego dnia i rodzaju dyżuru   OKOKOK
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

    # tworzenie tymczasowych instancji Person - tylko w celu wypełniania grafiku
    people = [PersonSchedule(one_schedule.person.name, one_schedule.one_schedule)
                          for one_schedule in one_schedules]

    # filtrowanie osób, które mają wolny dzień
    people_free_day = [person for person in people if person.wheather_day_is_free(day_number)]
    # print("people_free_day", people_free_day)

    # uzupełnienie grafiku o przykładowy dzień pracy - wedłóg day_number i work
    people_filled_example_work = []
    for person in people_free_day:
        person.take_work(day_number, work)       #  wprowadzanie zmian w grafiku
        people_filled_example_work.append(person)
    # print("people_filled_example_work", people_filled_example_work)

    # # filtrowanie osób na podstawie parametrów
    selected_person = [person for person in people_filled_example_work if
                     person.filtre_double_work() and
                     person.filtre_work_days_in_week(4) and
                     person.filtre_work_days_in_month(no_of_working_days)]

    # porządkowanie lisry osób ze względeu na liczbą przydzielonych dyżurów
    selected_person.sort(key=lambda person: person.get_working_days_number_person(), reverse=True)

    return [person.name for person in selected_person]


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
        print("day_number", day_number)

        # NIGHTS

        # liczba osób potrzebnych
        number_of_need_night = person_per_night - get_number_of_free_worktype(day_number, one_schedules, "N")
        # print(number_of_need_night)

        # tworzenie listy ludzi którzy mogą przyjąć dyżur    Wszystkie FILTRY !!!!!!!
        list_of_free_persons = get_free_people(day_number, one_schedules, "N", no_of_working_days)
        print("list_of_free_persons", list_of_free_persons)

        for night in range(number_of_need_night):
            # wybór osoby
            selected_person_name = list_of_free_persons.pop()

            # zdobycie numeru wylosowanej osoby w liście people
            selected_person_number = get_position_of_person(selected_person_name, one_schedules)
            print("selected_person_number", one_schedules[selected_person_number].person.name)

            # wprowadzenie zmiany do grafiku
            one_schedules[selected_person_number].take_work(day_number, "N")

        # DAYS

        # liczba osób potrzebnych
        number_of_need_days = person_per_day - get_number_of_free_worktype(day_number, one_schedules, "D")
        # print(number_of_need_days)

        # tworzenie listy ludzi którzy mogą przyjąć dyżur    Wszystkie FILTRY !!!!!!!
        list_of_free_persons = get_free_people(day_number, one_schedules, "D", no_of_working_days)
        print("list_of_free_persons", list_of_free_persons)

        for day in range(number_of_need_days):
            # wybór osoby
            selected_person_name = list_of_free_persons.pop()

            # zdobycie numeru wylosowanej osoby w liście people
            selected_person_number = get_position_of_person(selected_person_name, one_schedules)
            print("selected_person_number", one_schedules[selected_person_number].person.name)

            # wprowadzenie zmiany do grafiku
            one_schedules[selected_person_number].take_work(day_number, "D")

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