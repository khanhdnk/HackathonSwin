from math import atan
from django import forms
# import attrs
from django.shortcuts import render
# from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
# from .models import Notes
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView,DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect

class HomeView(TemplateView):
    template_name = 'index.html'
    # extra_context = {'today': datetime.today()}

class LoginCorrect(TemplateView):
    template_name = 'index.html'
class LogoutCorrect(LogoutView):
    next_page = '/'
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    username = forms.EmailField(
        label='Email:',
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Enter your username',
                'id' : 'form3Example3c',
                'class' : 'form-control',
            }
        )
    )

    first_name = forms.CharField(
        label='First Name:',
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Enter your first name',
                'id' : 'form3Example3c',
                'class' : 'form-control',
            }
        )
    )
    
    last_name = forms.CharField(
        label='Last Name:',
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Enter your last name',
                'id' : 'form3Example3c',
                'class' : 'form-control',
            }
        )
    )

    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(
            attrs = {
                'placeholder': 'Password',
                'id' : 'form3Example3c',
                'class' : 'form-control',
            }
        )
    )

    password2 = forms.CharField(
        label='Confirm Password', 
        widget=forms.PasswordInput(
            attrs = {
                'placeholder': 'Confirm Password',
                'id' : 'form3Example3c',
                'class' : 'form-control',
            }
        )
    )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = user.username
        user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Enter username',
                'class' : 'form-control form-control-lg'
            }
        )
    )

    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(
            attrs = {
                'placeholder': 'Enter password',
                'class' : 'form-control form-control-lg'
            }
        )
    )

class LoginInterfaceView(LoginView):
    template_name = 'SignIn.html'
    authentication_form = LoginForm
    success_url = '/'


class SignupView(CreateView):
    form_class = RegistrationForm
    template_name = 'SignUp.html'
    success_url = '/signin'
    #


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

class About(TemplateView):
    template_name = 'about.html'
class EditProfile(TemplateView):
    template_name = 'editprofile.html'
class Devices(TemplateView):
    template_name = 'devices.html'


