from django.test import TestCase

from .models import Schedule, OneSchedule
from . import solid_data as sd


class ScheduleTests(TestCase):
    """
    Test for method of Schedule model.
    """
    def test_get_month_calendar(self):
        """Test for method get_month_calendar for Schedule object.
        Should return list with info about days of the week for
        every days in month """

        schedule = Schedule(month="czerwiec", year='2016')
        expected_month_calendar_results = [
            (1, 'śr'), (2, 'cz'), (3, 'pt'), (4, 'so'), (5, 'n'),
            (6, 'pn'), (7, 'wt'), (8, 'śr'), (9, 'cz'), (10, 'pt'),
            (11, 'so'), (12, 'n'), (13, 'pn'), (14, 'wt'), (15, 'śr'),
            (16, 'cz'), (17, 'pt'), (18, 'so'), (19, 'n'), (20, 'pn'),
            (21, 'wt'), (22, 'śr'), (23, 'cz'), (24, 'pt'), (25, 'so'),
            (26, 'n'), (27, 'pn'), (28, 'wt'), (29, 'śr'), (30, 'cz')
        ]
        self.assertEqual(
            schedule.get_month_calendar(), expected_month_calendar_results
        )


def create_one_chedule(month_schedule):
    return OneSchedule(one_schedule=month_schedule)


class OneScheduleTests(TestCase):
    """
    Test for method of OneSchedule model.
    """

    def test_get_working_days_number_person(self):
        """Test for method get_working_days_number_person
        for OneSchedule object."""
        one_schedule = create_one_chedule('...DDD...NNN...DDD...NNN...DDD')
        self.assertEqual(one_schedule.get_working_days_number_person(), 15)

    def test_get_number_of_nights(self):
        """Test for method get_number_of_nights for OneSchedule object."""

        one_schedule = create_one_chedule('...DDD...NNN...DDD...NNN...DDD')
        self.assertEqual(one_schedule.get_number_of_nights(), 6)

    def test_get_number_of_days(self):
        """Test for method get_number_of_days for OneSchedule object."""

        one_schedule = create_one_chedule('...DDD...NNN...DDD...NNN...DDD')
        self.assertEqual(one_schedule.get_number_of_days(), 9)

    def test_wheather_day_is_free1(self):
        """Test for method wheather_day_is_free for OneSchedule object.
        - holiday"""
        one_schedule = create_one_chedule('UUUDDD...NNN...DDD...NNN...DDD')
        self.assertFalse(one_schedule.wheather_day_is_free(1))

    def test_wheather_day_is_free2(self):
        """Test for method wheather_day_is_free for OneSchedule object.
        - night"""
        one_schedule = create_one_chedule('UUUDDD...NNN...DDD...NNN...DDD')
        self.assertFalse(one_schedule.wheather_day_is_free(10))

    def test_wheather_day_is_free3(self):
        """Test for method wheather_day_is_free for OneSchedule object.
        - day"""
        one_schedule = create_one_chedule('UUUDDD...NNN...DDD...NNN...DDD')
        self.assertFalse(one_schedule.wheather_day_is_free(4))

    def test_wheather_day_is_free4(self):
        """Test for method wheather_day_is_free for OneSchedule object.
        - free day"""
        one_schedule = create_one_chedule('UUUDDD...NNN...DDD...NNN...DDD')
        self.assertTrue(one_schedule.wheather_day_is_free(7))

    def test_take_work1(self):
        """Test for method take_work for OneSchedule object - NIGHT"""
        one_schedule = create_one_chedule('...DDD...NNN...DDD...NNN...DDD')
        one_schedule.take_work(0, sd.NIGHT)
        self.assertEqual(
            one_schedule.one_schedule, 'N..DDD...NNN...DDD...NNN...DDD'
        )

    def test_take_work2(self):
        """Test for method take_work for OneSchedule object - DAY"""
        one_schedule = create_one_chedule('...DDD...NNN...DDD...NNN...DDD')
        one_schedule.take_work(7, sd.DAY)
        self.assertEqual(
            one_schedule.one_schedule, '...DDD.D.NNN...DDD...NNN...DDD'
        )

    def test_take_work3(self):
        """Test for method take_work for OneSchedule object - holiday"""
        one_schedule = create_one_chedule('...DDD...NNN...DDD...NNN...DDD')
        one_schedule.take_work(13, sd.HOLIDAY)
        self.assertEqual(
            one_schedule.one_schedule, '...DDD...NNN.U.DDD...NNN...DDD'
        )

    def test_filtre_work_days_in_month1(self):
        """Test for method filtre_work_days_in_month for OneSchedule object."""
        one_schedule = create_one_chedule('...DDD...NNN...DDD...NNN...DDD')
        self.assertFalse(one_schedule.filtre_work_days_in_month(14))

    def test_filtre_work_days_in_month2(self):
        """Test for method filtre_work_days_in_month for OneSchedule object."""
        one_schedule = create_one_chedule('...DDD...NNN...DDD...NNN...DDD')
        self.assertTrue(one_schedule.filtre_work_days_in_month(15))

    def test_filtre_double_work1(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('.D............................')
        self.assertFalse(one_schedule.filtre_double_work(0, 'N'))

    def test_filtre_double_work2(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('.D............................')
        self.assertTrue(one_schedule.filtre_double_work(0, 'D'))

    def test_filtre_double_work3(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('.N............................')
        self.assertTrue(one_schedule.filtre_double_work(0, 'N'))

    def test_filtre_double_work4(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('.N............................')
        self.assertTrue(one_schedule.filtre_double_work(0, 'D'))

    def test_filtre_double_work5(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('D.............................')
        self.assertTrue(one_schedule.filtre_double_work(1, 'N'))

    def test_filtre_double_work6(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('D.............................')
        self.assertTrue(one_schedule.filtre_double_work(1, 'D'))

    def test_filtre_double_work7(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('N.............................')
        self.assertTrue(one_schedule.filtre_double_work(1, 'N'))

    def test_filtre_double_work8(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('N.............................')
        self.assertFalse(one_schedule.filtre_double_work(1, 'D'))

    def test_filtre_double_work9(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('............D.................')
        self.assertTrue(one_schedule.filtre_double_work(11, 'D'))

    def test_filtre_double_work10(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('............D.................')
        self.assertFalse(one_schedule.filtre_double_work(11, 'N'))

    def test_filtre_double_work11(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('............N.................')
        self.assertFalse(one_schedule.filtre_double_work(13, 'D'))

    def test_filtre_double_work12(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('............N.................')
        self.assertTrue(one_schedule.filtre_double_work(13, 'N'))

    def test_filtre_double_work13(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('............................D.')
        self.assertTrue(one_schedule.filtre_double_work(29, 'D'))

    def test_filtre_double_work14(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('............................D.')
        self.assertTrue(one_schedule.filtre_double_work(29, 'N'))

    def test_filtre_double_work15(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('............................N.')
        self.assertFalse(one_schedule.filtre_double_work(29, 'D'))

    def test_filtre_double_work16(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('............................N.')
        self.assertTrue(one_schedule.filtre_double_work(29, 'N'))

    def test_filtre_double_work17(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('.............................D')
        self.assertTrue(one_schedule.filtre_double_work(28, 'D'))

    def test_filtre_double_work18(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('.............................D')
        self.assertFalse(one_schedule.filtre_double_work(28, 'N'))

    def test_filtre_double_work19(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('.............................N')
        self.assertTrue(one_schedule.filtre_double_work(28, 'D'))

    def test_filtre_double_work20(self):
        """Test for method filtre_double_work for OneSchedule object."""
        one_schedule = create_one_chedule('.............................N')
        self.assertTrue(one_schedule.filtre_double_work(28, 'N'))

    def test_filtre_work_days_in_week1(self):
        """Test for method filtre_work_days_in_week for OneSchedule object."""
        one_schedule = create_one_chedule('...DDD...NNN...DDD...NNN...DDD')
        self.assertTrue(one_schedule.filtre_work_days_in_week(4, 6))

    def test_filtre_work_days_in_week2(self):
        """Test for method filtre_work_days_in_week for OneSchedule object."""
        one_schedule = create_one_chedule('...DDD...NNN...DDD...NNN...DDD')
        self.assertTrue(one_schedule.filtre_work_days_in_week(4, 9))

    def test_filtre_work_days_in_week3(self):
        """Test for method filtre_work_days_in_week for OneSchedule object."""
        one_schedule = create_one_chedule('.N.DDD.D.NNN...DDD...NNN...DDD')
        self.assertFalse(one_schedule.filtre_work_days_in_week(4, 8))

    def test_filtre_work_days_in_week4(self):
        """Test for method filtre_work_days_in_week for OneSchedule object."""
        one_schedule = create_one_chedule('.N.DDD.D.NNN...DDD...NNN...DDD')
        self.assertFalse(one_schedule.filtre_work_days_in_week(4, 10))
