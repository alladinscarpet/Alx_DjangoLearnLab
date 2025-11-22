'''
DRF gives you ready-made class-based views like:
ListAPIView → handles GET list requests automatically
RetrieveAPIView → handles a single object GET
CreateAPIView → handles POST
ListCreateAPIView → handles GET + POST  on the same URL.
'''

from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, CreateAPIView
from .models import Book
from .serializers import BookSerializer

# Create your views here.

# entire “GET all books” API with only 3 lines of logic.
class BookList(ListAPIView):
    queryset = Book.objects.all() # tells the view what data to fetch from DB
    serializer_class = BookSerializer # tells DRF how to convert that data to JSON

'''# entire “GET + POST books” API with only 3 lines of logic.
class BookListCreate(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer'''

