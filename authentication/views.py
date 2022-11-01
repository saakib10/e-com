from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate,logout,login
from .form import *


def sign_in(request):
    cartItems = 0
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            form = UserSignupForm()

    else:
        form = UserSignupForm()
    contex = {'form':form,'cartItems':cartItems}
    return render(request,'signin.html',contex)

def log_in(request):
    cartItems = 0
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']

            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                form = AuthenticationForm()
                return HttpResponseRedirect('/')
    else:
        form = AuthenticationForm()

    contex = {'form':form,'cartItems':cartItems}
    return render(request,'login.html',contex)

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')