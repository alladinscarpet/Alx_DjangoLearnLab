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
from .models import Book

# drf
from rest_framework import generics
#from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, CreateAPIView
from .serializers import BookSerializer
from rest_framework import viewsets

# permission 4 view-set
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAdminOrReadOnly


# Create your views here.
#----------------------------------CBV----------------------------------------#
# entire “GET all books” API with only 3 lines of logic.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all() # tells the view what data to fetch from DB
    serializer_class = BookSerializer # tells DRF how to convert that data to JSON

'''# entire “GET + POST books” API with only 3 lines of logic.
class BookListCreate(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer'''

#-----------------------------View Set------------------------------------#
# viewSet for performing CRUD operations on Books(wrap multiple CBV methods into one class)
# ModelViewSet → complete set of CRUD operations for a model
# ReadOnlyModelViewSet → Offers read-only operations
# ViewSet → base class that allows you to define custom actions
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()          # what data this view set works with
    serializer_class = BookSerializer      # how data is converted to/from JSON

    #permission_classes = [IsAdminOrReadOnly] # allows anyone to read + only admin users can perform write operations
    permission_classes = [IsAuthenticated]  # <— only logged-in users can CRUD

'''
Think of CBVs as individual tools in a toolbox:
You pick one tool (CBV) for one task (GET, POST).
If you want to do 5 tasks, you pick 5 tools.
ViewSets are like a Swiss Army knife:
One tool that handles all the tasks for a model.
Router = the case that organizes the knife so you know which tool is available at which slot (URL).
'''
