from django.urls import path
from . import views

urlpatterns = [
    # ex: /api/books
    path('books/', views.BookList.as_view(), name='book-list'),
    #path('books/', views.BookListCreate.as_view(), name="book_list_create")

]