### Database Operations: Perform CRUD Operations in the Django Shell



### Objective
Learn how to perform and document basic **CRUD (Create, Read, Update, Delete)** operations in Django ORM using the Django shell.  
This exercise helps you understand how Django models interact with the database through Python commands.

---

```python
# Start Django shell
python manage.py shell

IPython 8.18.1 -- An enhanced Interactive Python. Type '?' for help.

# Import Book model
In [1]: from bookshelf.models import Book

# Check current Book records
In [2]: Book.objects.all()
Out[2]: <QuerySet []>

# --------------- CREATE ---------------#
# Create a Book instance
In [3]: b = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Verify creation
In [5]: Book.objects.all()
Out[5]: <QuerySet [<Book: '1984', written by George Orwell, released in 1949>]>


# ---------------- READ -----------------#
# Access book attributes
In [6]: b = Book.objects.get(title="Nineteen Eighty-Four")

In [7]: b.title
Out[7]: '1984'

In [8]: b.publication_year
Out[8]: 1949

# View internal dictionary
In [9]: b.__dict__
Out[9]:
{'_state': <django.db.models.base.ModelState at 0x203dd5e1fa0>,
 'id': 4,
 'title': '1984',
 'author': 'George Orwell',
 'publication_year': 1949}


# ------------------ UPDATE ------------------#
In [11]: book = Book.objects.get(title="1984")

# Update book title
In [12]: book.title = "Nineteen Eighty-Four"

# Verify update
In [13]: book.title
Out[13]: 'Nineteen Eighty-Four'

# Save changes
In [14]: book.save()

# View internal dictionary
In [15]: book.__dict__
Out[15]:
{'_state': <django.db.models.base.ModelState at 0x203dd5e1fa0>,
 'id': 4,
 'title': 'Nineteen Eighty-Four',
 'author': 'George Orwell',
 'publication_year': 1949}


# -------------------- DELETE -------------------#
# Retrieve book instance
In [16]: book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete book instance
In [17]: book.delete()
Out[17]: (1, {'bookshelf.Book': 1})

# Verify deletion
In [18]: Book.objects.all()
Out[18]: <QuerySet []>
