from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from django.views.generic.detail import DetailView
from .models import Library, Librarian, Author, Book


# Create your views here.

def index(request):
    """Function-based view that retrieves all books
       and renders a template displaying the list."""

    books = Book.objects.all() # Fetch all book instances from the database
    context = {"books": books}  # Create a context dictionary with book list
    return render(request, "relationship_app/list_books.html", context)


class LibraryDetailView(DetailView):
    """A class-based view for displaying details of a specific
       for a specific library, listing all books available in that library."""

    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"