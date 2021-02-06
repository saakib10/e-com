'''
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


class FormUserCreation(UserCreationForm):
    class Meta:
        model = User

        fields = ['username', 'first_name', 'email']
        labels = {'username': 'Username', 'email': 'Email', 'first_name': 'Mobile'}

'''