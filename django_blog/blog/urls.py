'''URL routing'''
from django.urls import path

# login/out
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # for register

#  e.g. when someone visits the root of this app (/rship/),
urlpatterns = [
    # ex: /blog/
    path("",views.index, name="index"),


# Auth routes
    # ex: /blog/login
    path('login/',  LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path("profile/", views.profile_view, name="profile")
]