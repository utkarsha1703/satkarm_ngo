from django.contrib import admin
from django.urls import path
from . import views
  

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),  
    path('signin', views.signin, name="signin"),  
    path('signout', views.signout, name="signout"),
    path("login", views.login, name="login"), 
    path('activate/<uidb64>/<token>', views.activate, name='activate'), 
]
