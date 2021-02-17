from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from django.contrib.auth.models import User

class UserSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email']
        labels = {'username':'Username','email':'Email'}