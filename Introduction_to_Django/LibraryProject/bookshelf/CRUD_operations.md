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

# --- CREATE ---
# Create a Book instance
In [3]: b = Book(title="1984", author="George Orwell", publication_year=1949)

# Save to database
In [4]: b.save()

# Verify creation
In [5]: Book.objects.all()
Out[5]: <QuerySet [<Book: '1984', written by George Orwell, released in 1949>]>

# --- READ ---
# Access book attributes
In [6]: b.title
Out[6]: '1984'

In [7]: b.author
Out[7]: 'George Orwell'

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

# --- UPDATE ---
# Update book title
In [10]: b.title = "Nineteen Eighty-Four"

# Verify update
In [11]: b.title
Out[11]: 'Nineteen Eighty-Four'

# Save changes
In [12]: b.save()

# Check updated dictionary
In [13]: b.__dict__
Out[13]:
{'_state': <django.db.models.base.ModelState at 0x203dd5e1fa0>,
 'id': 4,
 'title': 'Nineteen Eighty-Four',
 'author': 'George Orwell',
 'publication_year': 1949}

# --- DELETE ---
# Delete book instance
In [14]: b.delete()
Out[14]: (1, {'bookshelf.Book': 1})

# Verify deletion
In [15]: Book.objects.all()
Out[15]: <QuerySet []>
