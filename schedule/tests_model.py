

from django.test import TestCase

from .models import Schedule, OneSchedule
from .solid_data import *


class ScheduleTests(TestCase):
    """
    Test for method of Schedule model.
    """
    def test_get_month_calendar(self):
        """Test for method get_month_calendar for Schedule object.
        Should return list with info about days of the week for every days in month """

        schedule = Schedule(month="czerwiec", year='2016')
        expected_month_calendar_results = [
            (1, 'śr'), (2, 'cz'), (3, 'pt'), (4, 'so'), (5, 'n'),
            (6, 'pn'), (7, 'wt'), (8, 'śr'), (9, 'cz'), (10, 'pt'),
            (11, 'so'), (12, 'n'), (13, 'pn'), (14, 'wt'), (15, 'śr'),
            (16, 'cz'), (17, 'pt'), (18, 'so'), (19, 'n'), (20, 'pn'),
            (21, 'wt'), (22, 'śr'), (23, 'cz'), (24, 'pt'), (25, 'so'),
            (26, 'n'), (27, 'pn'), (28, 'wt'), (29, 'śr'), (30, 'cz')
        ]
        self.assertEqual(schedule.get_month_calendar(), expected_month_calendar_results)


class OneScheduleTests(TestCase):
    """
    Test for method of OneSchedule model.
    """
    def test_get_working_days_number_person(self):
        """Test for method get_working_days_number_person for OneSchedule object."""

        one_schedule = OneSchedule(one_schedule='...DDD...NNN...DDD...NNN...DDD')
        self.assertEqual(one_schedule.get_working_days_number_person(), 15)

    def test_get_number_of_nights(self):
        """Test for method get_number_of_nights for OneSchedule object."""

        one_schedule = OneSchedule(one_schedule='...DDD...NNN...DDD...NNN...DDD')
        self.assertEqual(one_schedule.get_number_of_nights(), 6)

    def test_get_number_of_days(self):
        """Test for method get_number_of_days for OneSchedule object."""

        one_schedule = OneSchedule(one_schedule='...DDD...NNN...DDD...NNN...DDD')
        self.assertEqual(one_schedule.get_number_of_days(), 9)

    def test_wheather_day_is_free(self):
        """Test for method wheather_day_is_free for OneSchedule object."""

        one_schedule = OneSchedule(one_schedule='...DDD...NNN...DDD...NNN...DDD')
        self.assertEqual(one_schedule.wheather_day_is_free(2), True)
        self.assertEqual(one_schedule.wheather_day_is_free(3), False)
        self.assertEqual(one_schedule.wheather_day_is_free(9), False)

    def test_take_work(self):
        """Test for method take_work for OneSchedule object."""

        one_schedule = OneSchedule(one_schedule='...DDD...NNN...DDD...NNN...DDD')
        one_schedule.take_work(0, NIGHT)
        one_schedule.take_work(7, DAY)
        self.assertEqual(one_schedule.one_schedule, 'N..DDD.D.NNN...DDD...NNN...DDD')

    def test_filtre_work_days_in_month(self):
        """Test for method filtre_work_days_in_month for OneSchedule object."""

        one_schedule = OneSchedule(one_schedule='...DDD...NNN...DDD...NNN...DDD')
        self.assertEqual(one_schedule.filtre_work_days_in_month(15), True)
        self.assertEqual(one_schedule.filtre_work_days_in_month(14), False)

    def test_filtre_double_work(self):
        """Test for method filtre_double_work for OneSchedule object."""

        one_schedule = OneSchedule(one_schedule='.D............................')
        self.assertEqual(one_schedule.filtre_double_work(0, 'N'), False)

        one_schedule = OneSchedule(one_schedule='.D............................')
        self.assertEqual(one_schedule.filtre_double_work(0, 'D'), True)

        one_schedule = OneSchedule(one_schedule='.N............................')
        self.assertEqual(one_schedule.filtre_double_work(0, 'N'), True)

        one_schedule = OneSchedule(one_schedule='.N............................')
        self.assertEqual(one_schedule.filtre_double_work(0, 'D'), True)

        one_schedule = OneSchedule(one_schedule='D.............................')
        self.assertEqual(one_schedule.filtre_double_work(1, 'N'), True)

        one_schedule = OneSchedule(one_schedule='D.............................')
        self.assertEqual(one_schedule.filtre_double_work(1, 'D'), True)

        one_schedule = OneSchedule(one_schedule='N.............................')
        self.assertEqual(one_schedule.filtre_double_work(1, 'N'), True)

        one_schedule = OneSchedule(one_schedule='N.............................')
        self.assertEqual(one_schedule.filtre_double_work(1, 'D'), False)

        one_schedule = OneSchedule(one_schedule='............D.................')
        self.assertEqual(one_schedule.filtre_double_work(11, 'D'), True)

        one_schedule = OneSchedule(one_schedule='............D.................')
        self.assertEqual(one_schedule.filtre_double_work(11, 'N'), False)

        one_schedule = OneSchedule(one_schedule='............N.................')
        self.assertEqual(one_schedule.filtre_double_work(13, 'D'), False)

        one_schedule = OneSchedule(one_schedule='............N.................')
        self.assertEqual(one_schedule.filtre_double_work(13, 'N'), True)

    def test_filtre_work_days_in_week(self):
        """Test for method filtre_work_days_in_week for OneSchedule object."""

        one_schedule = OneSchedule(one_schedule='...DDD...NNN...DDD...NNN...DDD')
        self.assertEqual(one_schedule.filtre_work_days_in_week(4, 6), True)
        self.assertEqual(one_schedule.filtre_work_days_in_week(4, 9), True)

        one_schedule = OneSchedule(one_schedule='.N.DDD.D.NNN...DDD...NNN...DDD')
        self.assertEqual(one_schedule.filtre_work_days_in_week(4, 8), False)
        self.assertEqual(one_schedule.filtre_work_days_in_week(4, 10), False)
