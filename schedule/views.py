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
    10: "6 x dyżur 12h + 3h 50",
    11: "6 x dyżur 12h + 11h 25",
    12: "7 x dyżur 12h + 7h 0",
    13: "8 x dyżur 12h + 2h 35",
    14: "8 x dyżur 12h + 10h 10",
    15: "9 x dyżur 12h + 5h 45",
    16: "10 x dyżur 12h + 1h 20",
    17: "10 x dyżur 12h + 8h 55",
    18: "11 x dyżur 12h + 4h 30",
    19: "12 x dyżur 12h + 0h 05",
    20: "12 x dyżur 12h + 7h 40",
    21: "13 x dyżur 12h + 3h 15",
    22: "13 x dyżur 12h + 10h 50",
    23: "14 x dyżur 12h + 6h 25",
    24: "15 x dyżur 12h + 2h 0"
}

WORKING_DAYS_NUMBERS = {
    10: 7, 11: 7, 12: 8, 13: 9, 14: 9, 15: 10, 16: 11, 17: 11,
    18: 12, 19: 13, 20: 13, 21: 14, 22: 14, 23: 15, 24: 16
}

DEFAULT_TEAM = ["" for elem in range(15)]
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


def main_context():
    default_context = {
        'months': MONTHS.values(),
        'years': YEARS,
        'current_month': current_month(),
        'current_year': current_year(),
        'teams': get_teams_from_db(),
        'schedule_names': get_schedule_names_from_db(),
        'default_team_name': today(),
        'dafault_team_size': DEFAULT_TEAM,

    }
    return default_context


# widok podstawowy
def main_page(request):
    context = main_context()
    return render(request, 'schedule/base.html', context)


def grafik_update(request):

    if request.POST:
        context = main_context()

        # Otwieranie okna służącego do wprowadzenia nowej załogi
        if "_new_team" in request.POST:

            # wyświetla stronę w celu utworzenia nowego zespołu
            print("NEW TEAM")
            return render(request, 'schedule/new_team.html', context)

        # Otwieranie okna służącego do edycji istniejącej załogi
        elif "_edit_team" in request.POST:
            try:
                team_to_edit = get_team_from_db(request.POST["edit_team"])

                context['Team'] = team_to_edit

                print("RENDEROWANIE STRONY Z EDYCJĄ TEAM", "Edycja team", team_to_edit, team_to_edit.pk)
                return HttpResponseRedirect(reverse('schedule:read_team', args=(team_to_edit.pk,)))

            except (KeyError, Team.DoesNotExist):
                return render(request, 'schedule/base.html', context)

        # usuwanie istniejącej załogi z bazy danych
        elif "_remove_team" in request.POST:
            try:
                team_to_remove = request.POST["edit_team"]
                remove_team(team_to_remove)
                context = main_context()

            except KeyError:
                context["error_message"] = "Wystąpił błąd podczas usuwania drużyny. " \
                                           "Najprawdopodobniej drużyna została już wcześniej " \
                                           "usunięta albo nie zapisana."

            return render(request, 'schedule/base.html', context)


class TeamDetailView(generic.DetailView):
    model = Team
    template_name = 'schedule/team.html'

    def get_context_data(self, **kwargs):

        # implementuje get_context_date z Clasy generic.DetailView
        context = super(TeamDetailView, self).get_context_data(**kwargs)

        # Dodaje pozostałą zawartość do context
        context.update(main_context())
        return context


def team_update(request):

    if request.POST:
        if "save_team" in request.POST:

            context = main_context()
            try:
                team_name = request.POST["team_name"].strip()

                crew, no = [], 0
                person_list = [key for key in request.POST.keys() if "person" in key]
                for person in person_list:
                    one_person = request.POST[person].strip()
                    if one_person:
                        crew.append(one_person)
                    else:
                        pass

            except KeyError:
                # wyświetlenie strony do wprowadzenia zespołu OD NOWA
                return render(request, 'schedule/new_team.html', context)

            if not team_name and not crew:
                context["error_message"] = "Wprowadź nazwę dla zespołu oraz imiona i nazwiska osób w zespole."
                return render(request, "schedule/new_team.html", context)

            elif not team_name:
                context["error_message"] = "Wprowadź nazwę dla zespołu."
                context["dafault_team_size"] = crew
                return render(request, "schedule/new_team.html", context)

            elif not crew:
                context["error_message"] = "Należy wprowadzić imiona i nazwiska osób w zespołe."
                context["default_team_name"] = team_name
                return render(request, "schedule/new_team.html", context)

            try:
                if team_name in [team.name for team in get_teams_from_db()]:
                    remove_team(team_name)
                save_team_to_db(team_name, crew)
            except:
                context["error_message"] = "Błąd podczas zapisu zespołu, sprawdź czy zespół o nazwie" \
                                           "'{}' już istnieje.".format(team_name)
                context["default_team_name"] = team_name
                context["dafault_team_size"] = crew
                return render(request, "schedule/new_team.html", context)

            team = get_team_from_db(team_name)
            return HttpResponseRedirect(reverse('schedule:read_team', args=(team.pk,)))





