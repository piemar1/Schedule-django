__author__ = 'marcin'

from .models import Team, Schedule



def get_team_names_from_db():
    """ Zwraca listę stringów z nazwami teams. """
    return [team.name for team in Team.objects.all()]


def get_schedule_names_from_db():
    """ Zwraca listę stringów z nazwami schedules. """
    return [schedule.name for schedule in Schedule.objects.all()]




def save_team_to_db(team):
    """
    Zapisuje team do bazy, Jako arg przyjmuje instancję Team.
    Jeżeli dany wpis w db już istnieje, usuwa poprzedni wpis i tworzy nowy.
    """
    pass


def save_schedule_to_db(schedule):
    """
    Zapisuje schedule do bazy, jako arg przyjmuję gotową instancję Schedule
    Jeżeli dany wpis w db już istnieje, usuwa poprzedni wpis i tworzy nowy.
    """
    pass




def delete_team_in_db(team_name_to_delete):
    """
    Usuwa wpis dla podanego team z bazy danych.
    """
    pass

def delete_schedule_in_db(schedule_name_to_delete):
    """
    Usuwa wpis dla podanego schedule z bazy danych.
    """
    pass


def get_team_from_db(team_name_to_read):
    """
    Zwraca instancję Team na podstawie danych z db, jako arg przyjmuje team_name.
    """
    pass


def get_schedule_from_db(schedule_name_to_read):
    """Zwraca instancję Schedule na podstawie danych z db, jako arg przyjmuje schedule_name."""
    pass



