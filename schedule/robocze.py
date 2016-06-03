__author__ = 'marcin'

import datetime
import calendar

MONTHS = {
    1:u"styczeń", 2:u"luty", 3:u"marzec", 4:u"kwiecień", 5:u"maj", 6:u"czerwiec",
    7:u"lipiec", 8:u"sierpień", 9:u"wrzesień", 10:u"październik", 11:u"listopad", 12:u"grudzień"
}


def today():
    return datetime.date.today()


def now():
    return datetime.datetime.now()


def current_month():
    return MONTHS[now().month]


def current_year():
    return now().year


if __name__ == "__main__":
    print(current_year())
    print(current_month())