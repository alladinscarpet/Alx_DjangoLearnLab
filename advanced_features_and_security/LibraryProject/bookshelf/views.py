from django.shortcuts import render
from .models import Book

# permissions
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

# Create your views here.
# -----------------------views requiring permissions------------------------------#
# View Book List — requires can_view
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return HttpResponse("You can view book list!")

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
