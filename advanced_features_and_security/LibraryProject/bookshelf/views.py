'''
Where you define what should happen when someone visits
a certain web page (the logic behind routes).
'''

from django.shortcuts import render
from .models import Book

# permissions
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

# secure form ORM usage
from .forms import ExampleForm



# Create your views here.
# -----------------------views requiring permissions------------------------------#
# Create Book — requires can_create
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return HttpResponse("You can create a book!")

# Edit Book — requires can_edit
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    return HttpResponse(f"You can edit book {book_id}!")

# Delete Book — requires can_delete
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    return HttpResponse(f"You can delete book {book_id}!")


# -----------------------views 4 secure forms------------------------------#
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # Using Django forms to validate user input and avoid SQL injection
    form = ExampleForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            books = books.filter(title__icontains=query)

    return render(request, "bookshelf/book_list.html", {"books": books, "form": form})


def some_view(request):
    response = HttpResponse("Hello")
    response["Content-Security-Policy"] = "default-src 'self';"
    return response