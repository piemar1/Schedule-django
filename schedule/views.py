                  # -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'

from django.shortcuts import render, HttpResponseRedirect, redirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.sessions.models import Session

from django.http import HttpResponse

from .models import *
import datetime
import calendar


"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
uporządkować if i else w template w html !!!!!!!!!!!!!!!!!!!!!!!!

"""



MONTHS = [
    u"styczeń", u"luty", u"marzec", u"kwiecień", u"maj", u"czerwiec", u"lipiec",
    u"sierpień", u"wrzesień", u"październik", u"listopad", u"grudzień"
]

WEEK_DAYS = {
    0: u"pn", 1: u"wt", 2: u"śr", 3: u"cz", 4: u"pt", 5: u"so", 6: u"n"
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
    return MONTHS[now().month-1]


def current_year():
    return now().year


def get_month_calendar(selected_year, selected_month):

    """
    Funkcja zwraca listę z planem miesiąca, zawierającą informację o liczbie dni
    oraz poszczególnych dniach tygodniach.
    """
    n = MONTHS.index(selected_month) + 1
    week_day, day_no = calendar.monthrange(selected_year, n)

    week_days = []
    for day in range(day_no):
        week_days.append(WEEK_DAYS[week_day])
        week_day += 1
        if week_day == 7:
            week_day = 0

    month_calendar = list(zip([elem + 1 for elem in range(day_no)], week_days))
    return month_calendar


def get_number_of_working_days_month(month_calendar):
    """
    Funckcja zwraca liczbę dni roboczych w danym miesiącu
    """
    number = 0
    for no, day in month_calendar:
        if day in WORKING_DAYS:
            number += 1
    return number


def main_context():
    default_context = {
        'months': MONTHS,
        'years': YEARS,
        'current_month': current_month(),
        'current_year': current_year(),
        'teams': Team.objects.all(),
        'schedules': Schedule.objects.all(),
        'default_team_name': today(),
        'default_schedule_name': today(),
        'dafault_team_size': DEFAULT_TEAM,
        'possible_no_of_person_night': range(10),
        'possible_no_of_person_day': range(10),
        'dafoult_no_of_person_night': 2,
        'dafoult_no_of_person_day': 4,
        'work': WORK,
        "working_days_number_text": [el[1] for el in WORKING_DAYS_NUMBER.values()],
    }
    return default_context


# widok podstawowy
def main_page(request):
    context = main_context()
    return render(request, 'schedule/base.html', context)


# widok nowego zespołu
def new_team(request):
    context = main_context()
    return render(request, 'schedule/new_team.html', context)


# działanie przycisków w głównym oknie programu
def grafik_update(request):

    if request.POST:
        context = main_context()

        # Otwieranie okna służącego do wprowadzenia nowej załogi
        if "_new_team" in request.POST:
            print("NEW TEAM")
            return HttpResponseRedirect('/schedule/new_team/')

        # Otwieranie okna służącego do edycji istniejącej załogi
        elif "_edit_team" in request.POST:
            try:
                team_to_edit = Team.objects.get(name=request.POST["edit_team"])

                # print("RENDEROWANIE STRONY Z EDYCJĄ TEAM", "Edycja team", team_to_edit, team_to_edit.pk)
                return HttpResponseRedirect(reverse('schedule:team', args=(team_to_edit.pk,)))

            except (KeyError, Team.DoesNotExist):
                return render(request, 'schedule/base.html', context)

        # usuwanie istniejącej załogi z bazy danych
        elif "_remove_team" in request.POST:
            try:
                team = Team.objects.get(name=request.POST["edit_team"])
                team.delete()

            except KeyError:
                context = main_context()
                context["error_message"] = "Wystąpił błąd podczas usuwania drużyny. " \
                                           "Najprawdopodobniej drużyna została już wcześniej " \
                                           "usunięta albo nie zapisana."
                return render(request, 'schedule/base.html', context)

            return HttpResponseRedirect('/schedule/')

        # Otwieranie okna do wprowadzenia nowego grafiku
        elif "_new_schedule" in request.POST:
            print("Tworzenie nowgo grafiku pracy")

            try:
                selected_month = request.POST['month']
                selected_year = int(request.POST['year'])
                team_name_for_new_schedule = request.POST["team_for_new_schedule"]
                month_calendar = get_month_calendar(selected_year, selected_month)

                request.session["team_name"] = team_name_for_new_schedule
                request.session["month_calendar"] = month_calendar
                request.session["selected_month"] = selected_month
                request.session["selected_year"] = selected_year
                return HttpResponseRedirect('/schedule/new_schedule/')

            except:
                context["error_message"] = "Wystąpił nieoczekiwany błąd."
                return render(request, 'schedule/base.html', context)

        elif "_remove_schedule" in request.POST:
            print("Usuwanie grafiku pracy z DB")
            try:
                schedule = Schedule.objects.get(name=request.POST["schedule_to_edit"])
                schedule.delete()
                return HttpResponseRedirect('/schedule/')

            except KeyError:
                context = main_context()
                context["error_message"] = "Wystąpił błąd podczas usuwania grafiku. " \
                                           "Najprawdopodobniej grafik został już wcześniej " \
                                           "usunięty albo nie zapisany."
                return render(request, 'schedule/base.html', context)

        elif "_edit_schedule" in request.POST:
            try:
                schedule_to_edit = Schedule.objects.get(name=request.POST["schedule_to_edit"])

                # print("RENDEROWANIE STRONY Z EDYCJĄ SCHEDULE", "schedule_to_edit", schedule_to_edit , schedule_to_edit .pk)
                return HttpResponseRedirect('/schedule/' + str(schedule_to_edit.pk) + '/schedule/')

            except (KeyError, Schedule.DoesNotExist):
                return render(request, 'schedule/base.html', context)


# widok nowego grafiku
def new_schedule(request):
    context = main_context()
    context["month_calendar"] = request.session["month_calendar"]
    context["selected_month"] = request.session["selected_month"]
    context["selected_year"] = request.session["selected_year"]
    context['team'] = Team.objects.get(name=request.session["team_name"])
    context["working_days"] = WORKING_DAYS_NUMBER[get_number_of_working_days_month(request.session["month_calendar"])
                              ][1]

    return render(request, 'schedule/new_schedule.html', context)


# widok istniejącego grafiku
def existed_schedule(request, pk):

    current_schedule = Schedule.objects.get(pk=pk)

    month_calendar = current_schedule.get_month_calendar()
    one_schedules = current_schedule.oneschedule_set.all()
    small_schedules = [[one_schedule.person.name, one_schedule.one_schedule] for one_schedule in one_schedules]

    request.session["team_name"] = current_schedule.crew.name
    request.session["selected_month"] = current_schedule.month
    request.session["selected_year"] = current_schedule.year
    request.session["month_calendar"] = month_calendar

    context = main_context()
    context["month_calendar"] = month_calendar
    context["current_schedule"] = current_schedule
    context["small_schedules"] = small_schedules
    context["working_days"] = WORKING_DAYS_NUMBER[get_number_of_working_days_month(month_calendar)][1]

    # print(month_calendar)
    # print(current_schedule.month)
    # print(current_schedule.year)
    # print(current_schedule.oneschedule_set.all())
    # print(small_schedules)

    return render(request, 'schedule/schedule.html', context)


                    # widok istniejących zespołów
class TeamDetailView(generic.DetailView):
    model = Team
    template_name = 'schedule/team.html'

    def get_context_data(self, **kwargs):

        # implementuje get_context_date z Clasy generic.DetailView
        context = super(TeamDetailView, self).get_context_data(**kwargs)

        # Dodaje pozostałą zawartość do context
        context.update(main_context())
        return context


# obsługa przycisków w oknie z edycją drużyn
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
                if team_name in Team.objects.all():
                    team = Team.objects.get(name=team_name)
                    team.delete()

                a_team = Team(name=team_name)
                a_team.save()

                person_list = [Person(name=name) for name in crew]
                for person in person_list:
                    person.crew = a_team
                    person.save()

            except:
                context["error_message"] = "Błąd podczas zapisu zespołu, sprawdź czy zespół o nazwie" \
                                           "'{}' już istnieje.".format(team_name)
                context["default_team_name"] = team_name
                context["dafault_team_size"] = crew
                return render(request, "schedule/new_team.html", context)

            team = Team.objects.get(name=team_name)
            return HttpResponseRedirect(reverse('schedule:team', args=(team.pk,)))


# obsługa przycisków w widoku z edycją grafików
def schedule_update(request):

    if request.POST:

        selected_month = request.session["selected_month"]
        selected_year = request.session["selected_year"]
        month_calendar = request.session["month_calendar"]

        schedule_name = request.POST['schedule_name']
        team_for_new_schedule = Team.objects.get(name=request.session["team_name"])

        crew = team_for_new_schedule.person_set.all()

        # odczytywanie ze strony grafiku dla poszczególnych osób
        schedules = []
        for person in crew:
            person_schedule = []
            for no, day in month_calendar:
                one_day = request.POST[person.name + u'_day' + str(no)]
                person_schedule.append(one_day)
            schedules.append("".join(person_schedule))

        # zapisywanie grafiku
        if "_save_schedule" in request.POST:

            # usunięcie grafiku z bazy, jeśli istnieje już grafik o takiej nazwie
            if schedule_name in [schedule.name for schedule in Schedule.objects.all()]:
                schedule_to_delete = Schedule.objects.get(name=schedule_name)
                schedule_to_delete.delete()

            # stworzenie obiektu nowego grafiku
            current_schedule = Schedule(
                name=schedule_name,
                year=selected_year,
                month=selected_month,
                crew=team_for_new_schedule
            )
            # zapisuwanie grafiku do bazy danych
            current_schedule.save()

            # tworzenie obiektów OneSchedule wewnątrz grafiku
            one_schedules = [OneSchedule(one_schedule=person_schedule, schedule=current_schedule, person=person) for
                             person, person_schedule in zip(crew, schedules)]

            # zapisywanie obiektów OneSchedule wewnątrz grafiku do basy danych
            for one_schedule in one_schedules:
                one_schedule.save()

            return HttpResponseRedirect('/schedule/' + str(current_schedule.pk) + '/schedule/')

        if "_export_schedule_as_pdf" in request.POST:

            import io
            from .write_pdf import WritePDF

            # tworzenie obiektów OneSchedule wewnątrz grafiku
            one_schedules = [OneSchedule(one_schedule=person_schedule, person=person) for
                             person, person_schedule in zip(crew, schedules)]

            month_working_days = request.POST["no_of_working_days_in_nonth"]

            # month_working_days zwraca np "10 x dyżur 12h + 8h 55" a ja mam dostać 11

            no_of_workdays = ""
            for value in WORKING_DAYS_NUMBER.values():
                if month_working_days in value:
                    no_of_workdays = value[0]

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="grafik.pdf"'

            buffor = io.BytesIO()
            pdf_buffor = WritePDF(buffor, selected_year, selected_month, one_schedules,
                                  month_calendar, month_working_days, no_of_workdays)

            pdf_buffor.run()
            pdf = buffor.getvalue()
            buffor.close()
            response.write(pdf)

            return response

        if "_fill_schedule" in request.POST:


            person_per_day = int(request.POST["no_of_person_day"])
            person_per_night = int(request.POST["no_of_person_night"])
            month_working_days = request.POST["no_of_working_days_in_nonth"]

            no_of_workdays = ""
            for value in WORKING_DAYS_NUMBER.values():     # tę pętelkę można przerobić na ofobnego def jest używany w 2 miejscach
                if month_working_days in value:
                    no_of_workdays = value[0]

            one_schedules = [OneSchedule(one_schedule=person_schedule, person=person) for
                             person, person_schedule in zip(crew, schedules)]

            from .fill_schedule import fill_the_schedule

            number_of_tries = 1
            while number_of_tries:
                try:
                    print("POCZĄTEK WYPEŁNIANIA GRAFIKU !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    new_one_schedules = fill_the_schedule(one_schedules,
                                                          no_of_workdays,
                                                          person_per_day,
                                                          person_per_night)

                    for one_schedule in new_one_schedules:
                        print(one_schedule.person.name[:3], one_schedule.one_schedule)

                    small_schedules = [[one_schedule.person.name, one_schedule.one_schedule] for one_schedule in
                                       new_one_schedules]

                    context = main_context()
                    context["month_calendar"] = request.session["month_calendar"]
                    context["small_schedules"] = small_schedules
                    return render(request, 'schedule/schedule.html', context)


                except IndexError:
                    print("WYJĄTEK @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    number_of_tries -= 1













