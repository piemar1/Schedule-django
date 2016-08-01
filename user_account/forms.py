from django import forms

from user_account.models import User


class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'surname']
        widgets = {'password': forms.PasswordInput()}


class LogInForm(forms.Form):
    email = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())
    widgets = {'password': forms.PasswordInput()}


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'surname']

    new_password_1 = forms.CharField(max_length=30, min_length=8, required=False)
    new_password_2 = forms.CharField(max_length=30, min_length=8, required=False)
