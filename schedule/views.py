from django.shortcuts import render
from .models import Team, Schedule
# Create your views here.


import datetime
import calendar


MONTHS = [
    u"styczeń", u"luty", u"marzec", u"kwiecień", u"maj", u"czerwiec", u"lipiec",
    u"sierpień", u"wrzesień", u"październik", u"listopad", u"grudzień"
]

WEEK_DAYS = {
    0: u"pn", 1: u"wt", 2: u"śr", 3: u"cz", 4: u"pt", 5: u"so", 6: u"n"
}

WORKING_DAYS_NUMBER_TEXT = {
    10: "6 x dyżur 12h + 3h 50'",
    11: "6 x dyżur 12h + 11h 25'",
    12: "7 x dyżur 12h + 7h 0'",
    13: "8 x dyżur 12h + 2h 35'",
    14: "8 x dyżur 12h + 10h 10'",
    15: "9 x dyżur 12h + 5h 45'",
    16: "10 x dyżur 12h + 1h 20'",
    17: "10 x dyżur 12h + 8h 55'",
    18: "11 x dyżur 12h + 4h 30'",
    19: "12 x dyżur 12h + 0h 05'",
    20: "12 x dyżur 12h + 7h 40'",
    21: "13 x dyżur 12h + 3h 15'",
    22: "13 x dyżur 12h + 10h 50'",
    23: "14 x dyżur 12h + 6h 25'",
    24: "15 x dyżur 12h + 2h 0'"
}

WORKING_DAYS_NUMBERS = {
    10: 7, 11: 7, 12: 8, 13: 9, 14: 9, 15: 10, 16: 11, 17: 11,
    18: 12, 19: 13, 20: 13, 21: 14, 22: 14, 23: 15, 24: 16
}

TEAM_SIZE = 15
YEARS = range(2016, 2020)
WORK = (u"D", u"N", u'U', u".")
TYPE_OF_WORK = (u"D", u"N")
WORKING_DAYS = (u"pn", u"wt", u"śr", u"cz", u"pt")
NIGHT = u"N"
DAY = u"D"
FREE = u"."


def today():
    return datetime.date.today()


def now():
    return datetime.datetime.now()


def current_month():
    current_date = now()
    return MONTHS[now().month-1]


def current_year():
    current_date = now()
    return current_date.year


def get_team_names_from_db():
    teams = Team.objects.all()
    return [team.name for team in teams]


def get_schedule_names_from_db():
    schedules = Schedule.objects.all()
    return [schedule.name for schedule in schedules]


def main_page(request):
    context = {
        'months': MONTHS,
        'years': YEARS,
        'current_month': current_month(),
        'current_year': current_year(),
        'team_names': get_team_names_from_db(),
        'schedule_names': get_schedule_names_from_db()
    }
    return render(request, 'schedule/base.html', context)


def grafik_update(request):
    pass

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list
#     }
#     return render(request, 'polls/index.html', context)


# @app.route('/GrafikIwonki', methods=['GET', 'POST'])     # Pierwsza strona
# def main_page():
#     return render_template('Grafik Iwonki.html',
#                            months        = MONTHS,
#                            years         = YEARS,
#                            current_month = CURRENT_MONTH,
#                            current_year  = CURRENT_YEAR,
#                            team_names    = get_team_names_from_db(),
#                            schedule_names= get_schedule_names_from_db())



