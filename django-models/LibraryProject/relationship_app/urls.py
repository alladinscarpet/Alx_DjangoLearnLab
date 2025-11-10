'''URL routing'''

from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # for register

#  e.g. when someone visits the root of this app (/rship/),
#
urlpatterns = [
    # ex: /rship/
    path("",list_books, name="index"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),

    # Auth routes
    path('login/',  LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

]
