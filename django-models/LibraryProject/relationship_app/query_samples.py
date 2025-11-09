import os
import django
import sys

# Add project directory to the Python path
project_path = 'C:\\Users\\deninjo\\OneDrive\\Desktop\\Python\\ALX\\Alx_DjangoLearnLab\\django-models\\LibraryProject'
sys.path.append(project_path)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

# import models
from relationship_app.models import Author, Book, Library, Librarian  # FIXED IMPORT

'''
# populate db first

a1 = Author.objects.create(name="Marcel Proust")

b1 = Book.objects.create(title="Swann's Way", author=a1)

library = Library.objects.create(name="McMillan Memorial Library")
library.books.add(b1)

librarian = Librarian.objects.create(name="Mary Jane", library=library)
'''


# Query all books by a specific author
print("Query all books by a specific author...")
author_name = "Amy Tan"
author = Author.objects.get(name=author_name)
#books = author.books.all()
books = Book.objects.filter(author=author)  # Using filter
print(books)
print()


# List all books in a library.
print("Query & list all books in a library....")
library_name = "Ba Sing Se Central Library"
library = Library.objects.get(name=library_name)
lib_books = library.books.all()
for book in lib_books:
    print(book)
print()


# Retrieve the librarian for a library
print("Retrieve the librarian for a library....")
library = Library.objects.get(name=library_name)
ln = library.librarian
print(ln)




