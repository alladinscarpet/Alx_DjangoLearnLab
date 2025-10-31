### **3. Update a Book Record**



#### **Objective**
Learn how to modify and save changes to existing database records using Django ORM.  
This task demonstrates how to update field values of a model instance.

---

#### **Command**
Update the title of **“1984”** to **“Nineteen Eighty-Four”** and save the changes.

---

#### **Steps**

```python
In [11]: b.title = "Nineteen Eighty-Four"

In [12]: b.title
Out[12]: 'Nineteen Eighty-Four'

In [13]: b.save()

In [14]: b.__dict__
Out[14]:
{'_state': <django.db.models.base.ModelState at 0x203dd5e1fa0>,
 'id': 4,
 'title': 'Nineteen Eighty-Four',
 'author': 'George Orwell',
 'publication_year': 1949}
