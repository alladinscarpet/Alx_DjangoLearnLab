'''URL routing'''

from django.urls import path
from .views import list_books, LibraryDetailView

# login/out
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # for register

# role restricted views
from .views import admin_view, librarian_view, member_view


#  e.g. when someone visits the root of this app (/rship/),
#
urlpatterns = [
    # ex: /rship/
    path("",list_books, name="index"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),

    # Auth routes
    # ex: /rship/login
    path('login/',  LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # role-restricted  routes
    # ex: /rship/member-view
    path("admin-view/", admin_view, name="admin-view"),
    path("librarian-view/", librarian_view, name="librarian-view"),
    path("member-view/", member_view, name="member-view"),

]
