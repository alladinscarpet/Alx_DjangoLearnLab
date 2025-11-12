'''
Where you define what should happen when someone visits
a certain web page (the logic behind routes).
'''

from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views.generic.detail import DetailView
from .models import Library, Librarian, Author, Book

# to log the user in right after registration
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# role restricted views
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

# enforce permissions
from django.contrib.auth.decorators import permission_required

# user-input forms
from .forms import CreateAuthorForm, CreateBookForm


# Create your views here:
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
        form = UserCreationForm(request.POST) # built-in form that validates username + password
        if form.is_valid():
            user = form.save()     # creates the user with hashed password
            login(request, user)   # starts a session so user is logged in
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


#========================custom role-based access control (RBAC)===============================#
# <<<<<<<<<<<Helper functions to check role>>>>>>>>>>>>
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

def is_admin_or_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role in ['Admin', 'Librarian']


# <<<<<<<<<<<<<actual role-restricted views>>>>>>>>>>>>>>>>
# Only Admins can access admin_view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")



# Only Librarians can access librarian_view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@user_passes_test(is_admin_or_librarian)
def create_author(request):
    if request.method == 'POST':
        form = CreateAuthorForm(request.POST) # to pass data to form
        if form.is_valid():
            author = form.save()
            # Redirect to book creation, passing author id in URL
            return redirect('add-book', author_id=author.id)
    else:
        form = CreateAuthorForm()
    # for GET request display empty form
    return render(request, 'relationship_app/create_author.html', {'form': form})

@user_passes_test(is_admin_or_librarian)
def create_book(request, author_id):
    author = Author.objects.get(id=author_id)

    if request.method == 'POST':
        form = CreateBookForm(request.POST)
        if form.is_valid():
            # Set the author before saving
            book = form.save(commit=False)
            book.author = author
            book.save()
            return redirect('index')  # or anywhere else
    else:
        # Pre-fill the author field, but hide it from user if you prefer
        form = CreateBookForm(initial={'author': author})

    return render(request, 'relationship_app/create_book.html', {'form': form, 'author': author})




# Only Members can access member_view
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")
# If a user without permission tries, Django redirects them to the login page.






#-----------------Enforce Permissions------------------#
# Add a book (only users with can_add_book can access)
@permission_required('relationship_app.can_add_book') # checks if current logged-in user has that permission.
def add_book(request):
    # Logic for adding a book (form handling)
    return HttpResponse("You can add a book!")


# Edit a book (only users with can_change_book)
@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    # Logic for editing a book
    return HttpResponse(f"You can edit book {book_id}!")


# Delete a book (only users with can_delete_book)
@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    # Logic for deleting a book
    return HttpResponse(f"You can delete book {book_id}!")
