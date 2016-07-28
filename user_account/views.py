import random, hashlib

from django.shortcuts import get_object_or_404, render_to_response, HttpResponseRedirect, redirect, render, HttpResponse
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.decorators import login_required

from .forms import NewUserForm, LogInForm, EditUserForm
from .models import User
from .multiform import MultiFormsView
from yourworkschedule.settings import EMAIL_HOST_USER, HOST_NAME


# import pdb;pdb.set_trace()


# Działa dodawanie, wysłanie maila  i aktywowanie konta user
#
# Wprowadziłem zmiany w modelu user ale bez migracji
# nie działa logowanie i autenticate


class NewUserView(MultiFormsView):
    template_name = "user_account/log_or_new_account.html"
    success_url = reverse_lazy('user_account:success_created')
    form_classes = {'new_user': NewUserForm,
                    'login': LogInForm}

    def get_context_data(self, **kwargs):

        # implementuje get_context_date z Clasy generic.DetailView
        context = super(NewUserView, self).get_context_data(**kwargs)
        if 'user_is_active' in self.request.session:
            context['user_is_active'] = self.request.session['user_is_active']
        if 'user_is_none' in self.request.session:
            context['user_is_none'] = self.request.session['user_is_none']
        return context

    def new_user_form_valid(self, form):

        # print("form.cleaned_data", form.cleaned_data)
        new_user = form.save()
        new_user.set_password(form.cleaned_data["password"])

        h = hashlib.sha1()
        h.update(str(random.random()).encode('utf-8'))
        salt = h.hexdigest()[:5]

        h = hashlib.sha1()
        text = salt+new_user.name
        h.update(text.encode('utf-8'))

        new_user.activation_key = h.hexdigest()
        new_user.save()

        subject = "Your Work Schedule: Confirm registration"
        text = "Hi %s, \n please confirm Your registration by clicking or copy-past this link \n" \
               "%s/user_account/activate/%s/ \n Please confirm with in 48 houers. Thank You for using our app."\
               "\n Your Sandbox Team" % (new_user.name, HOST_NAME, new_user.activation_key)
        send_mail(subject, text, EMAIL_HOST_USER, [new_user.email], fail_silently=False)
        # print("WYSŁANO MAIL !!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return HttpResponseRedirect(self.get_success_url())

    def login_form_valid(self, form):

        self.request.session['user_is_none'] = None
        self.request.session['user_is_active'] = None

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        profile = get_object_or_404(User, email=email)
        # przygotować widok 404 gdy nie podano nieprawidłowy login i lub hasło

        if user is None:
            self.request.session['user_is_none'] = True
            return HttpResponseRedirect('/user_account/')

        elif user.active is False:
            self.request.session['user_is_active'] = False
            return HttpResponseRedirect('/user_account/')
        else:
            self.request.session['user_is_active'] = True
            self.request.session['user_is_none'] = False
            login(self.request, user)
        return HttpResponseRedirect('/user_account/home/')


def activate(request, activation_key):
    profile = get_object_or_404(User, activation_key=activation_key)
    if profile.akey_expires < timezone.now():
        return render('user_account/activate.html', {'expired': True})
    profile.save(update_fields=['active', 'activation_key'])
    return render('user_account/activate.html', {'success': True,
                                                 'name': profile.name + " " + profile.surname})

@login_required()
def HomeView(request):
    return HttpResponseRedirect('/schedule/')

    # redirect('/schedule/')



# class HomeView(generic.ListView):
#     template_name = 'user_account/home.html'
#     context_object_name = 'User_list'
#     model = User


def logout_view(request):
    logout(request)
    return render_to_response('user_account/logout.html')



# DO ZROBIENIA, NIE DZIAŁA PRAWIDŁOWO !!!!!!!!!!!!!!!!!!
# brak edycji konta oraz usuwania konta
# @login_required()
def edit_user_view(request):
    template_name = "user_account/user_edit.html"
    form = EditUserForm(request.POST or None, instance=request.user)
    request.session['edit_succes'] = False

    if form.is_valid():
        print("form.cleaned_data", form.cleaned_data)

        if request.user.is_authenticated():
            print(request.user.name, "USER IS LOGED IN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        new_user_data = form.save()
        new_user_data.set_password(form.cleaned_data['new_password_1'])
        new_user_data.save()
        request.session['edit_succes'] = True
        # return redirect('/user_account/user_edit/')
        return HttpResponseRedirect('/user_account/user_edit/')

        # return HttpResponse('/user_account/user_edit/')


    # nie działa context i session

    edit_state = request.session['edit_succes']
    return render(request, template_name, {'form': form,
                                           'edit_succes': True})






















