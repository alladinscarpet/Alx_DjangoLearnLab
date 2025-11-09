### **2. Retrieve Book Attributes**


#### **Objective**
Understand how to access and display model instance attributes in Django ORM.  
This task focuses on retrieving and viewing all the fields of the book created in `create.md`

---

#### **Command**
Retrieve and display all attributes of the book you just created.

---

#### **Steps**

```python

In [6]: b = Book.objects.get(title="Nineteen Eighty-Four")

In [7]: b.title
Out[7]: '1984'

In [8]: b.author
Out[8]: 'George Orwell'

In [9]: b.publication_year
Out[9]: 1949

In [10]: b.__dict__
Out[10]:
{'_state': <django.db.models.base.ModelState at 0x203dd5e1fa0>,
 'id': 4,
 'title': '1984',
 'author': 'George Orwell',
 'publication_year': 1949}
