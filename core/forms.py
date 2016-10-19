from django import forms
from django.contrib.auth.models import User
from django.forms import widgets

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=widgets.PasswordInput())
        