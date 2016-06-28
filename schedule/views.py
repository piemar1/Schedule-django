# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'


import datetime
import calendar

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Team, Schedule, Person, OneSchedule
from .solid_data import *


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


def get_no_of_workdays(month_working_days):
    """
    Funkcja zwraca liczbę dużurów do zrealizowania dla na podstawie opisu liczby dużurów w miesiącu.
    """
    for value in WORKING_DAYS_NUMBER.values():
        if month_working_days in value:
            return value[0]
    return


def main_context():
    """
    Funkcja zwraca podstawową zawartość context.
    """
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
            return HttpResponseRedirect('/schedule/new_team/')

        # Otwieranie okna służącego do edycji istniejącej załogi
        elif "_edit_team" in request.POST:
            team_to_edit = get_object_or_404(Team, name=request.POST["edit_team"])
            return HttpResponseRedirect(reverse('schedule:team', args=(team_to_edit.pk,)))

        # usuwanie istniejącej załogi z bazy danych
        elif "_remove_team" in request.POST:
            team_to_remove = get_object_or_404(Team, name=request.POST["edit_team"])
            team_to_remove.delete()
            return HttpResponseRedirect('/schedule/')

        # Otwieranie okna do wprowadzenia nowego grafiku
        elif "_new_schedule" in request.POST:
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

            except KeyError:
                context["error_message"] = "Wystąpił nieoczekiwany błąd podczas tworzenia nowego grafiku." \
                                           "Sróbuj ponownie. Jeśli błąd będzie się powtarzał, " \
                                           "skontaktuj się z administratorem."
                return render(request, 'schedule/base.html', context)

        # usunięcie istniejącego grafiku z bazy danych
        elif "_remove_schedule" in request.POST:
            schedule = get_object_or_404(Schedule, name=request.POST["schedule_to_edit"])
            schedule.delete()
            return HttpResponseRedirect('/schedule/')

        # edycja istniejącego grafiku z bazy danych
        elif "_edit_schedule" in request.POST:
            schedule_to_edit = get_object_or_404(Schedule, name=request.POST["schedule_to_edit"])
            return HttpResponseRedirect('/schedule/' + str(schedule_to_edit.pk) + '/schedule/')


# widok nowego grafiku
def new_schedule(request):

    context = main_context()
    month_calendar = request.session["month_calendar"]
    context["month_calendar"] = month_calendar
    context["selected_month"] = request.session["selected_month"]
    context["selected_year"] = request.session["selected_year"]
    context["working_days"] = WORKING_DAYS_NUMBER[get_number_of_working_days_month(month_calendar)][1]
    context['team'] = Team.objects.get(name=request.session["team_name"])
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

        # zapisywanie drużyny do bazy danych
        if "save_team" in request.POST:
            context = main_context()
            try:
                team_name = request.POST["team_name"].strip()
                # czytanie obecnej drużyny z widoku
                person_list = [key for key in request.POST.keys() if "person" in key]
                crew = [request.POST[person].strip() for person in person_list if request.POST[person].strip()]

            except KeyError:
                # wyświetlenie strony do wprowadzenia zespołu od nowa
                return render(request, 'schedule/new_team.html', context)

            # W przyszłości planuję napisać ten fragment w JavaScript
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
                # usuwanie team z bazy danych jeśli istnieje team o zadanej nazwie
                if team_name in [team.name for team in Team.objects.all()]:
                    team = Team.objects.get(name=team_name)
                    team.delete()

                # zapisanie team do bazy danych
                a_team = Team(name=team_name)
                a_team.save()

                # zapisanie osób przyporządkowanych do team w bazie danych
                person_list = [Person(name=name) for name in crew]
                for person in person_list:
                    person.crew = a_team
                    person.save()

            except:
                context["error_message"] = "Wystąpił błąd podczas zapisu zespołu {}. Sprubuj ponownie." \
                                           "Jeżeli sytuacja będzie się powtarzać spoknatkuj się z " \
                                           "administratorem.".format(team_name)
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
        team_for_new_schedule = get_object_or_404(Team, name=request.session["team_name"])

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

            try:
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

            except KeyError:
                context = main_context()
                context["current_schedule_name"] = schedule_name
                context["month_calendar"] = month_calendar
                context["working_days"] = WORKING_DAYS_NUMBER[get_number_of_working_days_month(month_calendar)][1]
                context["small_schedules"] = [[person.name, schedule] for person, schedule in zip(crew, schedules)]

                context["error_message"] = "Wystąpił błąd podczas zapisu grafiku {}. Sprubuj ponownie." \
                                           "Jeżeli sytuacja będzie się powtarzać spoknatkuj się z " \
                                           "administratorem.".format(schedule_name)
                return render(request, 'schedule/schedule.html', context)

        # export grafiku do pliku pdf
        if "_export_schedule_as_pdf" in request.POST:

            import io
            from .write_pdf import WritePDF

            # tworzenie obiektów OneSchedule wewnątrz grafiku
            one_schedules = [OneSchedule(one_schedule=person_schedule, person=person) for
                             person, person_schedule in zip(crew, schedules)]

            month_working_days = request.POST["no_of_working_days_in_nonth"]
            no_of_workdays = get_no_of_workdays(month_working_days)

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

        # automatyczne wypełnianie grafiku wedlug zadanych parametrów
        if "_fill_schedule" in request.POST:

            context = main_context()
            # schedule_name = request.POST['schedule_name']
            # month_calendar = request.session["month_calendar"]
            context["current_schedule_name"] = schedule_name
            context["month_calendar"] = month_calendar
            context["working_days"] = WORKING_DAYS_NUMBER[get_number_of_working_days_month(month_calendar)][1]

            person_per_day = int(request.POST["no_of_person_day"])
            person_per_night = int(request.POST["no_of_person_night"])
            month_working_days = request.POST["no_of_working_days_in_nonth"]

            no_of_workdays = get_no_of_workdays(month_working_days)
            one_schedules = [OneSchedule(one_schedule=person_schedule, person=person) for
                             person, person_schedule in zip(crew, schedules)]

            from .fill_schedule import fill_the_schedule

            number_of_tries = 10
            while number_of_tries:
                try:
                    new_one_schedules = fill_the_schedule(one_schedules, no_of_workdays,
                                                          person_per_day, person_per_night)

                    context["small_schedules"] = [[one_schedule.person.name, one_schedule.one_schedule]
                                                  for one_schedule in new_one_schedules]
                    return render(request, 'schedule/schedule.html', context)

                except IndexError:
                    number_of_tries -= 1

            context["error_message"] = "Atomatyczne uzupełnienie grafiku {} nie powiodło się !!! ;-(" \
                                       "Zalecamy zmianę parametrów automatycznego uzupełniania grafiku " \
                                       "na mniej wymagające.".format(schedule_name)
            context["small_schedules"] = [[person.name, schedule] for person, schedule in zip(crew, schedules)]
            return render(request, 'schedule/schedule.html', context)
