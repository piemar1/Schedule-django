# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'


months = (
    ("styczeń", "styczeń"),
    ("luty", "luty"),
    ("marzec", "marzec"),
    ("kwiecień", "kwiecień"),
    ("maj", "maj"),
    ("czerwiec", "czerwiec"),
    ("lipiec", "lipiec"),
    ("sierpień", "sierpień"),
    ("wrzesień", "wrzesień"),
    ("październik", "październik"),
    ("listopad", "listopad"),
    ("grudzień", "grudzień")
)

years = (
    ('2016', '2016'),
    ('2017', '2017'),
    ('2018', '2018'),
    ('2019', '2019'),
    ('2020', '2020')
)

WEEK_DAYS = {
    0: "pn",
    1: "wt",
    2: "śr",
    3: "cz",
    4: "pt",
    5: "so",
    6: "n"
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
WORKING_DAYS = ("pn", "wt", "śr", "cz", "pt")
WORK = ("D", "N", 'U', ".")
TYPE_OF_WORK = ("D", "N")
NIGHT = "N"
DAY = "D"
FREE_DAY = "."
HOLIDAY = "U"
