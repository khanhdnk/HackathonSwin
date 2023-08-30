from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.HomeView, name="home"),
    path("signin/", views.SignIn, name="Signin"),
    path("signup/", views.SignUp, name="Signup"),
]
