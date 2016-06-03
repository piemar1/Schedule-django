# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'

from django.shortcuts import render, HttpResponseRedirect, redirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import *

import datetime
import calendar


MONTHS = {
    1: u"styczeń", 2: u"luty", 3: u"marzec", 4: u"kwiecień", 5: u"maj", 6: u"czerwiec",
    7: u"lipiec", 8: u"sierpień", 9: u"wrzesień", 10: u"październik", 11: u"listopad", 12: u"grudzień"
}

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
    return MONTHS[now().month]


def current_year():
    return now().year


MAIN_CONTEXT = {
    'months': MONTHS.values(),
    'years': YEARS,
    'current_month': current_month(),
    'current_year': current_year(),
    'size': range(TEAM_SIZE),
    'teams': get_teams_from_db(),    # zwraca obiekty Team !!!!
    'schedule_names': get_schedule_names_from_db()
}


def main_context():
    main_context = {
        'months': MONTHS.values(),
        'years': YEARS,
        'current_month': current_month(),
        'current_year': current_year(),
        'size': range(TEAM_SIZE),
        'teams': get_teams_from_db(),  # zwraca obiekty Team !!!!
        'schedule_names': get_schedule_names_from_db()
    }
    return main_context


# widok podstawowy
def main_page(request):
    context = MAIN_CONTEXT
    return render(request, 'schedule/base.html', context)


def grafik_update(request):

    if request.POST:

        # Otwieranie okna służącego do wprowadzenia nowej załogi
        if "_new_team" in request.POST:

            # wyświetla stronę w celu utworzenia nowego zespołu
            context = main_context()
            print("NEW TEAM")
            return render(request, 'schedule/new_team.html', context)

        # Otwieranie okna służącego do edycji istniejącej załogi
        elif "_edit_team" in request.POST:   # DO UZUPEŁNIENIA !!!!!!!!!!!!1
            print("EDYCJA TEAM")
            try:
                team_to_edit = request.POST["edit_team"]
                print("team_to_edit", team_to_edit)
                team_to_edit = get_team_from_db(team_to_edit)

                context = main_context()
                context['Team'] = team_to_edit

                print("RENDEROWANIE STRONY Z EDYCJĄ TEAM", "Edycja team", team_to_edit, team_to_edit.pk)

                # a_crew = Team.Person_set.all()
                # print("a_crew", a_crew)
                # return HttpResponse('schedule:read_team')
                # return render(request, 'schedule/team.html', context)
                return HttpResponseRedirect(reverse('schedule:read_team', args=(team_to_edit.pk,)))

                # return redirect('schedule/team.html', {'Team': team_to_edit})

            except:
                print("WYJĄTEK podczas edycji team")


        elif "_remove_team" in request.POST:
            # usuwanie istniejącej załogi z bazy danych
            context = main_context()
            try:
                team_to_remove = request.POST["edit_team"]
                remove_team(team_to_remove)
                context = main_context()
                # context['teams']=get_teams_from_db()

            except KeyError:
                context["error_message"] = "Wystąpił błąd podczas usuwania drużyny. " \
                                           "Najprawdopodobniej drużyna została już wcześniej " \
                                           "usunięta albo nie zapisana."

            return render(request, 'schedule/base.html', context)




class TeamDetailView(generic.DetailView):
    model = Team
    template_name = 'schedule/team.html'



def team_update(request):

    if request.POST:
        if "save_team" in request.POST:


            print("request.POST", request.POST)
            context = main_context()
            try:
                print("czytanie nazwy team")
                team_name = request.POST["team_name"].strip()

                print("czytanie crew")
                crew, no = [], 0
                while 1:
                    person = request.POST["person" + str(no)].strip()
                    if not person:
                        pass
                    else:
                        crew.append(person)
                    no += 1

            except KeyError:
                print("KeyError 1")
                # wyświetlenie strony do wprowadzenia zespołu OD NOWA
                # return render(request, 'schedule/new_team.html', context)

            if not team_name and not crew:
                context["error_message"] = "Wprowadź nazwę dla zespołu oraz imiona i nazwiska osób w zespole."
                return render(request, "schedule/new_team.html", context)

            elif not team_name:
                context["error_message"] = "Wprowadź nazwę dla zespołu."
                return render(request, "schedule/new_team.html", context)

            elif not crew:
                context["error_message"] = "Należy wprowadzić imiona i nazwiska osób w zespołe."
                return render(request, "schedule/new_team.html", context)

            try:
                save_team_to_db(team_name, crew)
                print("ZAPISANE !!!!!!!!!!!!!!!!", team_name, crew)
            except:
                 pass # wyświetlenie strony z info team o danej nazwie juz istnieje !!!!!!!!!

            team = get_team_from_db(team_name)
            return HttpResponseRedirect(reverse('schedule:read_team'))

























