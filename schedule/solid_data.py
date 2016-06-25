# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'


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

WEEK_DAYS = {
    0: u"pn",
    1: u"wt",
    2: u"śr",
    3: u"cz",
    4: u"pt",
    5: u"so",
    6: u"n"
}

WORKING_DAYS_NUMBER = {
    10: [7, "6 x dyżur 12h + 3h 50"],
    11: [7, "6 x dyżur 12h + 11h 25"],
    12: [8, "7 x dyżur 12h + 7h 0"],
    13: [9, "8 x dyżur 12h + 2h 35"],
    14: [9, "8 x dyżur 12h + 10h 10"],
    15: [10, "9 x dyżur 12h + 5h 45"],
    16: [11, "10 x dyżur 12h + 1h 20"],
    17: [11, "10 x dyżur 12h + 8h 55"],
    18: [12, "11 x dyżur 12h + 4h 30"],
    19: [13, "12 x dyżur 12h + 0h 05"],
    20: [13, "12 x dyżur 12h + 7h 40"],
    21: [14, "13 x dyżur 12h + 3h 15"],
    22: [14, "13 x dyżur 12h + 10h 50"],
    23: [15, "14 x dyżur 12h + 6h 25"],
    24: [16, "15 x dyżur 12h + 2h 0"]
}

MONTHS = [m[0] for m in months]
YEARS = range(2016, 2020)
DEFAULT_TEAM = ["" for elem in range(15)]
WORKING_DAYS = (u"pn", u"wt", u"śr", u"cz", u"pt")
WORK = (u"D", u"N", u'U', u".")
TYPE_OF_WORK = (u"D", u"N")
NIGHT = u"N"
DAY = u"D"
FREE_DAY = u"."
