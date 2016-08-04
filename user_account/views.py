__author__ = 'Marcin Pieczyński'

import random, hashlib

from django.shortcuts import get_object_or_404, render_to_response, HttpResponseRedirect, render
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import NewUserForm, LogInForm, EditUserForm
from .models import User
from .multiform import MultiFormsView
from yourworkschedule.settings import EMAIL_HOST_USER, HOST_NAME


class NewUserView(MultiFormsView):
    """
    Base generic view for user login or registration.
    """
    template_name = "user_account/log_or_new_account.html"
    success_url = reverse_lazy('user_account:success_created')
    form_classes = {
        'new_user': NewUserForm,
        'login': LogInForm
    }

    def get_context_data(self, **kwargs):
        """
        Method for get_context_date implementing from generic.DetailView class.
        """
        context = super(NewUserView, self).get_context_data(**kwargs)
        if 'user_is_active' in self.request.session:
            context['user_is_active'] = self.request.session['user_is_active']
        if 'user_is_none' in self.request.session:
            context['user_is_none'] = self.request.session['user_is_none']
        return context

    def new_user_form_valid(self, form):
        """
        Method for new user registration.
        """
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
        text = """
        Hi {}, \n please confirm Your registration by clicking or copy-past this link \n
        {}/user_account/activate/{}/ \n Please confirm with in 48 houers. Thank You for using our app.
        \n Your Sandbox Team
        """.format(new_user.name, HOST_NAME, new_user.activation_key)

        send_mail(
            subject,
            text,
            EMAIL_HOST_USER,
            [new_user.email],
            fail_silently=False
        )
        return HttpResponseRedirect(self.get_success_url())

    def login_form_valid(self, form):
        """
        Method for user login.
        """
        self.request.session.update({
            'user_is_none': None,
            'user_is_active': None
        })

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            self.request.session['user_is_none'] = True
            return HttpResponseRedirect('/user_account/')
        elif user.active is False:
            self.request.session['user_is_active'] = False
            return HttpResponseRedirect('/user_account/')
        else:
            self.request.session.update({'user_is_none': False, 'user_is_active': True})
            login(self.request, user)
        return HttpResponseRedirect('/schedule/')


def activate(request, activation_key):
    """
    View function for user account activation.
    """
    profile = get_object_or_404(User, activation_key=activation_key)
    if profile.akey_expires < timezone.now():
        return render('user_account/activate.html', {'expired': True})

    profile.save(update_fields=['active', 'activation_key'])
    return render('user_account/activate.html', {'success': True,
                                                 'name': profile.name + " " + profile.surname})


@login_required()
def home_view(request):
    """
    Home view, redirection to the base schedule view.
    """
    return HttpResponseRedirect('/schedule/')


def logout_view(request):
    """
    Logout view.
    """
    logout(request)
    return render_to_response('user_account/logout.html')


@login_required()
def edit_user_view(request):
    """
    User detail view for profile editing.
    """
    template_name = "user_account/user_edit.html"
    form = EditUserForm(request.POST or None, instance=request.user)

    if form.is_valid():

        new_user_data = form.save()
        if form.cleaned_data['new_password_1']:
            new_user_data.set_password(form.cleaned_data['new_password_1'])
            request.session['new_password'] = True

        new_user_data.save()
        update_session_auth_hash(request, request.user)  # enable change of user password without logout
        request.session['edit_succes'] = True
        return HttpResponseRedirect('/user_account/user_edit/')

    edit_state = request.session['edit_succes'] if 'edit_succes' in request.session else None
    new_password = request.session['new_password'] if 'new_password' in request.session else None
    request.session.update({'edit_succes': None, 'new_password': None})

    return render(request, template_name, {'form': form,
                                           'edit_succes': edit_state,
                                           'new_password': new_password})