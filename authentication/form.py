from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from django.contrib.auth.models import User
from store.models import Customer

class UserSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email','first_name']
        labels = {'username':'Username','first_name':'Mobile Number','email':'Email'}


    def save(self,commit = True):
        customer = Customer()
        instance = super(UserSignupForm,self).save(commit=commit)
        customer.user = instance
        customer.name = instance.username
        customer.email = instance.email
        customer.mobile = instance.first_name
        customer.save()