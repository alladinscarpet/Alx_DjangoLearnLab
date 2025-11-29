'''
Where you define what should happen when someone visits
a certain web page (the logic behind routes).


DRF gives you ready-made class-based views like:
ListAPIView → handles GET list requests automatically
RetrieveAPIView → handles a single object GET
CreateAPIView → handles POST
ListCreateAPIView → handles GET + POST  on the same URL.

ViewSets encapsulate the logic for common CRUD operations
'''

from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly

# Create your views here.

# LIST ALL BOOKS
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # public access


# RETRIEVE ONE BOOK
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # public access

# CREATE BOOK
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]  # allows anyone to read + only admin users can perform write operations

    # Customize create + update behavior
    # where you can add logic like:
    # tagging who created the book
    # sanitizing input
    # filtering fields
    def perform_create(self, serializer):
        # Add extra behavior here if needed
        data = serializer.validated_data
        data['title'] = data['title'].title()  # capitalize properly
        serializer.save()


# UPDATE BOOK
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]  # allows anyone to read + only admin users can perform write operations

    def perform_update(self, serializer):
        # Add extra behavior here if needed
        serializer.save() # literally does nothing extra(saves the data exactly as it is)

# DELETE BOOK
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAdminOrReadOnly]  # allows anyone to read + only admin users can perform write operations


