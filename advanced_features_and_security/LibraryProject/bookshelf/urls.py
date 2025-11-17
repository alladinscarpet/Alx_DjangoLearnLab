from django.urls import path
from . import views

urlpatterns = [
    # ex: /bookshelf/
    path("books/", views.book_list, name="book-list"),

    # permission routes
    # ex: /bookshelf/create
    path("books/create/", views.create_book, name="create-book"),
    path("books/<int:book_id>/edit/", views.edit_book, name="edit-book"),
    path("books/<int:book_id>/delete/", views.delete_book, name="delete-book"),
]
