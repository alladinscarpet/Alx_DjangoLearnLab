from django.urls import path, include
from . import views

# view set for drf
from rest_framework.routers import DefaultRouter

# Create router
# Router automatically generates all the necessary URLs for each CRUD action:
router = DefaultRouter()
router.register(r'books_all', views.BookViewSet, basename='book_all')  # 'books_all' becomes the URL prefix


# Define URL patterns
urlpatterns = [
    # ex: /api/books
    path('books/', views.BookList.as_view(), name='book-list'),
    #path('books/', views.BookListCreate.as_view(), name="book_list_create")

    # router handles all CRUD URLs
    # ex: /books_all/
    # ex: /books_all/<id>/
    path('', include(router.urls)),
]