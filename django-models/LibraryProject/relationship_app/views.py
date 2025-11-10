from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from django.views.generic.detail import DetailView
from .models import Library, Librarian, Author, Book

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login  # to log the user in right after registration
from django.contrib.auth.decorators import login_required


# Create your views here.

def list_books(request):
    """Function-based view that retrieves all books
       and renders a template displaying the list."""

    books = Book.objects.all() # Fetch all book instances from the database
    context = {"books": books}  # Create a context dictionary with book list
    return render(request, "relationship_app/list_books.html", context)


class LibraryDetailView(DetailView):
    """A class-based view for displaying details of a specific
       for a specific library, listing all books available in that library."""

    # DetailView is a Django class-based view designed to show one specific object.
    model = Library # Fetch a Library object from the database based on the ID in the URL.
    template_name = "relationship_app/library_detail.html" # tells Django which HTML file to render.
    context_object_name = "library" # gives the template a clean variable name

    # its usage - in urls.py, .as_view() converts the class into a callable view function


def register(request):
    """
    GET  -> show empty registration form
    POST -> validate and create user, then log them in
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()     # creates the user with hashed password
            login(request, user)   # starts a session so user is logged in
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})