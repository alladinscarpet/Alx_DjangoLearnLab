### **4. Delete a Book Record**


#### **Objective**
Understand how to remove existing records from the database using Django ORM.  
This task focuses on deleting a model instance and confirming its removal.

---

#### **Command**
Delete the book you created and confirm the deletion by trying to retrieve all books again.

---

#### **Steps**

```python
# Import Book model
In [1]: from bookshelf.models import Book

In [16]: book = Book.objects.get(title="Nineteen Eighty-Four")

In [17]: book.delete()
Out[17]: (1, {'bookshelf.Book': 1})

In [18]: Book.objects.all()
Out[18]: <QuerySet []>
