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
In [15]: b.delete()
Out[15]: (1, {'bookshelf.Book': 1})

In [16]: Book.objects.all()
Out[16]: <QuerySet []>
