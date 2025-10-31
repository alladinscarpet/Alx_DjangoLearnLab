### **1. Create a Book Instance**


#### **Objective**
Learn how to create and save a new record in the database using Django ORM.  
This task introduces how to instantiate model objects and persist them to the database.

---

#### **Command**
Create a Book instance with the title **“1984”**, author **“George Orwell”**, and publication year **1949**.

---

#### **Steps**

```python
In [1]: from bookshelf.models import Book

In [2]: Book.objects.all()
Out[2]: <QuerySet []>

In [3]: b = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

In [4]: b.save()

In [5]: Book.objects.all()
Out[5]: <QuerySet [<Book: '1984', written by George Orwell, released in 1949>]>
