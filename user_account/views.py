import random, hashlib

from django.views import generic
from django.core.mail import send_mail

from django.shortcuts import get_object_or_404, render_to_response, render, redirect

from .forms import NewUserForm, LogInForm
from .models import User
from yourworkschedule.settings import EMAIL_HOST_USER, HOST_NAME
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout


class NewUserView(generic.CreateView):
    template_name = "user_account/new_account.html"
    success_url = reverse_lazy('user_account:success_created')
    form_class = NewUserForm

    def form_valid(self, form):
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
        return super(NewUserView, self).form_valid(form)


def activate(request, activation_key):
    profile = get_object_or_404(User, activation_key=activation_key)
    if profile.akey_expires < timezone.now():
        return render_to_response('user_account/activate.html', {'expired': True})
    profile.save(update_fields=['active', 'activation_key'])
    return render_to_response('user_account/activate.html', {'success': True})


class LogInView(generic.FormView):
    template_name = "user_account/login.html"
    form_class = LogInForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user.active:
            login(self.request, user)
        return redirect('user_account/home.html', {'success': True})


def logout_view(request):
    logout(request)
    return redirect('user_account/home.html', {'success': True})