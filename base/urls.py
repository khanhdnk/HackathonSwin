from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('signin', views.LoginInterfaceView.as_view(), name="signin"),
    path('logout', views.LogoutCorrect.as_view(), name='logout'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('logintrue', views.LoginCorrect.as_view(), name='logintrue'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('editprofile', views.EditProfile.as_view(), name='edit'),

    path('about', views.About.as_view(), name='about'),
    path('devices', views.Devices.as_view(), name="devices")

]

