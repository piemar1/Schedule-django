# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'


import datetime
import calendar

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from user_account.models import User
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

    return list(zip([elem + 1 for elem in range(day_no)], week_days))


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


def get_user_teams(request):
    return Team.objects.filter(user=request.user)


def get_user_schedules(request):
    return Schedule.objects.filter(user=request.user)


def main_context(request):
    """
    Funkcja zwraca podstawową zawartość context.
    """
    default_context = {
        'months': MONTHS,
        'years': YEARS,
        'current_month': current_month(),
        'current_year': current_year(),
        'teams': get_user_teams(request),
        'schedules': get_user_schedules(request),
        'default_team_name': today(),
        'default_schedule_name': today(),
        'dafault_team_size': DEFAULT_TEAM,
        'possible_no_of_person_night': range(10),
        'possible_no_of_person_day': range(10),
        'dafoult_no_of_person_night': 2,
        'dafoult_no_of_person_day': 2,
        'work': WORK,
        "working_days_number_text": [el[1] for el in WORKING_DAYS_NUMBER.values()],
    }
    return default_context


@login_required()
def main_page(request):
    """
    Base schedule view.
    """
    context = main_context(request)
    return render(request, 'schedule/_base.html', context)


@login_required()
def new_team(request):
    """
    New Team view.
    """
    context = main_context(request)
    return render(request, 'schedule/new_team.html', context)


class TeamDetailView(LoginRequiredMixin, generic.TemplateView):
    """
    Generic view of existing Team.
    """

    template_name = 'schedule/team.html'

    def get_context_data(self, **kwargs):
        # Implementing get_context_date from generic.DetailView class

        context = super(TeamDetailView, self).get_context_data(**kwargs)
        context.update(main_context(self.request))
        team_to_edit = get_object_or_404(Team, name=self.request.session["team_name_to_edit"])
        context['team'] = team_to_edit
        return context


def grafik_update(request):
    """"
    Function with button action in main schedule view.
    """
    if request.POST:
        context = main_context(request)

        # Otwieranie okna służącego do wprowadzenia nowej załogi
        if "_new_team" in request.POST:
            return HttpResponseRedirect('/schedule/new_team/')

        # Otwieranie okna służącego do edycji istniejącej załogi
        elif "_edit_team" in request.POST:
            team_to_edit = get_object_or_404(Team, name=request.POST["edit_team"])
            request.session["team_name_to_edit"] = team_to_edit.name
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

                request.session.update({
                    "team_name": team_name_for_new_schedule,
                    "month_calendar": month_calendar,
                    "selected_month": selected_month,
                    "selected_year": selected_year
                })
                return HttpResponseRedirect('/schedule/new_schedule/')

            except KeyError:
                context["error_message"] = "Wystąpił nieoczekiwany błąd podczas tworzenia nowego grafiku." \
                                           "Sróbuj ponownie. Jeśli błąd będzie się powtarzał, " \
                                           "skontaktuj się z administratorem."
                return render(request, 'schedule/base.html', context)

        # usunięcie istniejącego grafiku z bazy danych
        # TODO removing or deletion in case of lack schedules --> 404, hould be message

        elif "_remove_schedule" in request.POST:
            schedule = get_object_or_404(Schedule, name=request.POST["schedule_to_edit"])
            schedule.delete()
            return HttpResponseRedirect('/schedule/')

        # edycja istniejącego grafiku z bazy danych
        elif "_edit_schedule" in request.POST:
            schedule_to_edit = get_object_or_404(Schedule, name=request.POST["schedule_to_edit"])
            return HttpResponseRedirect('/schedule/' + str(schedule_to_edit.pk) + '/schedule/')


@login_required()
def new_schedule(request):
    """
    View of new schedule.
    """
    context = main_context(request)
    month_calendar = request.session["month_calendar"]
    context.update({
        "month_calendar": month_calendar,
        "selected_month": request.session["selected_month"],
        "selected_year": request.session["selected_year"],
        "working_days": WORKING_DAYS_NUMBER[
            get_number_of_working_days_month(month_calendar)][1],
        "team": Team.objects.get(name=request.session["team_name"])
    })
    return render(request, 'schedule/new_schedule.html', context)


@login_required()
def existed_schedule(request, pk):
    """
    View of existing schedule from database.
    """
    current_schedule = Schedule.objects.get(pk=pk)

    month_calendar = current_schedule.get_month_calendar()
    one_schedules = current_schedule.oneschedule_set.all()
    small_schedules = [[one_schedule.person.name, one_schedule.one_schedule]
                       for one_schedule in one_schedules]

    request.session.update({
        "team_name": current_schedule.crew.name,
        "selected_month": current_schedule.month,
        "selected_year": current_schedule.year,
        "month_calendar": month_calendar
    })

    context = main_context(request)
    context.update({
        "month_calendar": month_calendar,
        "current_schedule": current_schedule,
        "small_schedules": small_schedules,
        "working_days": WORKING_DAYS_NUMBER[
            get_number_of_working_days_month(month_calendar)][1]
    })
    return render(request, 'schedule/schedule.html', context)


def team_update(request):
    """"
    Function with button action in team view.
    """
    if request.POST:

        # zapisywanie drużyny do bazy danych
        if "save_team" in request.POST:
            context = main_context(request)
            try:
                team_name = request.POST["team_name"].strip()
                # odczytanie obecnej drużyny z widoku
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
                if team_name in [team.name for team in get_user_teams(request)]:
                    team = Team.objects.get(name=team_name, user=request.user)
                    team.delete()

                # zapisanie team do bazy danych
                a_team = Team(
                    name=team_name,
                    user=request.user
                )
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
                context.update({
                    "default_team_name": team_name,
                    "dafault_team_size": crew
                })
                return render(request, "schedule/new_team.html", context)

            team = Team.objects.get(name=team_name)
            request.session["team_name_to_edit"] = team.name
            return HttpResponseRedirect(reverse('schedule:team', args=(team.pk,)))


def schedule_update(request):
    """"
    Function with button action in schedule view.
    """
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
                one_day = request.POST[person.name + '_day' + str(no)]
                person_schedule.append(one_day)

            schedules.append(''.join(person_schedule))

        # zapisywanie grafiku
        if "_save_schedule" in request.POST:

            try:
                # usunięcie grafiku z bazy, jeśli istnieje już grafik o takiej nazwie
                if schedule_name in [schedule.name for schedule in get_user_schedules(request)]:
                    schedule_to_delete = Schedule.objects.get(name=schedule_name, user=request.user)
                    schedule_to_delete.delete()

                # stworzenie obiektu nowego grafiku
                current_schedule = Schedule(
                    name=schedule_name,
                    year=selected_year,
                    month=selected_month,
                    crew=team_for_new_schedule,
                    user=request.user
                )
                # zapisuwanie grafiku do bazy danych
                current_schedule.save()

                # tworzenie obiektów OneSchedule wewnątrz grafiku
                one_schedules = [
                    OneSchedule(
                        one_schedule=person_schedule,
                        schedule=current_schedule,
                        person=person
                    ) for person, person_schedule in zip(crew, schedules)
                ]

                # zapisywanie obiektów OneSchedule wewnątrz grafiku do basy danych
                for one_schedule in one_schedules:
                    one_schedule.save()

                return HttpResponseRedirect('/schedule/' + str(current_schedule.pk) + '/schedule/')

            except KeyError:
                context = main_context(request)
                context.update({
                    "current_schedule_name": schedule_name,
                    "month_calendar": month_calendar,
                    "working_days": WORKING_DAYS_NUMBER[get_number_of_working_days_month(month_calendar)][1],
                    "small_schedules": [[person.name, schedule] for person, schedule in zip(crew, schedules)],
                    "error_message": "Wystąpił błąd podczas zapisu grafiku {}. Sprubuj ponownie."
                                     "Jeżeli sytuacja będzie się powtarzać spoknatkuj się z "
                                     "administratorem.".format(schedule_name)
                })
                return render(request, 'schedule/schedule.html', context)

        else:
            # tworzenie obiektów OneSchedule wewnątrz grafiku

            one_schedules = [
                OneSchedule(
                    one_schedule=person_schedule,
                    person=person
                ) for person, person_schedule in zip(crew, schedules)
            ]

            month_working_days = request.POST["no_of_working_days_in_nonth"]
            no_of_workdays = get_no_of_workdays(month_working_days)

            # export grafiku do pliku pdf
            if "_export_schedule_as_pdf" in request.POST:

                import io
                from .write_pdf import WritePDF

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
            elif "_fill_schedule" in request.POST:

                context = main_context(request)
                context.update({
                    "current_schedule_name": schedule_name,
                    "month_calendar": month_calendar,
                    "working_days": WORKING_DAYS_NUMBER[get_number_of_working_days_month(month_calendar)][1]
                })

                person_per_day = int(request.POST["no_of_person_day"])
                person_per_night = int(request.POST["no_of_person_night"])

                from .fill_schedule import fill_the_schedule

                number_of_tries = 10

                ###################### PRINTY
                print("data before filling schedules ")
                for one in one_schedules:
                    print("one_schedule", one.person, one.one_schedule, one.schedule)
                print("no_of_workdays", no_of_workdays)
                print("person_per_day", person_per_day)
                print("person_per_night", person_per_night)
                ###################### PRINTY

                while number_of_tries:
                    try:
                        new_one_schedules = fill_the_schedule(one_schedules, no_of_workdays,
                                                              person_per_day, person_per_night)

                        context["small_schedules"] = [[one_schedule.person.name, one_schedule.one_schedule]
                                                      for one_schedule in new_one_schedules]
                        return render(request, 'schedule/schedule.html', context)

                    except IndexError:
                        number_of_tries -= 1

                context.update({
                    "error_message": "Atomatyczne uzupełnienie grafiku {} nie powiodło się !!! ;-("
                                     "Zalecamy zmianę parametrów automatycznego uzupełniania grafiku "
                                     "na mniej wymagające.".format(schedule_name),
                    "small_schedules": [[person.name, schedule] for person, schedule in zip(crew, schedules)]
                })
                return render(request, 'schedule/schedule.html', context)
