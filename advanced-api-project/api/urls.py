from django.urls import path, include
from . import views

# Define URL patterns
urlpatterns = [
    # ex: GET /api/books
    path('books/', views.BookListView.as_view(), name='book-list'),

    # ex: GET api/books/<pk>/
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),

    # ex: POST api/books/create/
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),

    # ex: PUT/PATCH api/books/<pk>/update/
    path('books/update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),

    # ex: DELETE api/books/<pk>/delete/
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),
]