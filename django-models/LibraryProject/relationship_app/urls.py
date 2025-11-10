'''URL routing'''

from django.urls import path
from .views import list_books, LibraryDetailView

# login/out
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # for register

# role restricted views
from .views import admin_view, librarian_view, member_view

# enforce permissions
from .views import add_book, edit_book, delete_book


#  e.g. when someone visits the root of this app (/rship/),
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

    # role-permission  routes
    # ex: /rship/books/add
    path('books/add_book/', add_book, name='add-book'),
    path('books/<int:book_id>/edit_book/', edit_book, name='edit-book'),
    path('books/<int:book_id>/delete_book/', delete_book, name='delete-book'),

]
