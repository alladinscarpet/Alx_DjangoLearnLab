### 4. Implementing Custom Permissions in Django



#### Objective
Implement custom permissions in your Django application to control access to specific actions such as adding, editing, and deleting book entries based on user roles.  
This task will guide you through creating these permissions in the model and enforcing them in views.

---

#### Task Description
In the **`relationship_app`** of your Django project, extend the existing `Book` model to include custom permissions.  
You will then update the views to enforce these permissions, ensuring that only authorized users can perform certain actions.

---

#### Steps

1. **Extend the `Book` Model with Custom Permissions**

   Add custom permissions to the `Book` model to specify who can add, edit, or delete the entries.

   - **Model Changes Required:**
     - Inside the `Book` model, define a nested **`Meta`** class.
     - Within this `Meta` class, specify a **`permissions`** tuple that includes permissions like `can_add_book`, `can_change_book`, and `can_delete_book`.

2. **Update Views to Enforce Permissions**

   Adjust your views to check if a user has the necessary permissions before allowing them to perform create, update, or delete operations.

   - **Views to Modify:**
     - Use Django's **`permission_required`** decorator to secure views that add, edit, or delete books.
     - For each view, apply the corresponding permission.

3. **Define URL Patterns for Secured Views**

   Ensure that the secured views are accessible through specific URLs.  
   Set up these URLs in your **`urls.py`** file and ensure they are properly named for clarity.

   - **URLs to Setup:**
     - Create distinct paths for adding, editing, and deleting books.
     - Link each path to its respective view with the appropriate permissions.

---

#### Deliverables

1. **`models.py`**: Update the `Book` model to include a `Meta` class with defined custom permissions.
2. **`views.py`**: Implement permission checks in the views that handle book creation, modification, and deletion.
3. **`urls.py`**: Configure and submit the URL patterns that map to the secured views.

---

#### Instructions for Each File

- **`models.py`**:  
  In the `Book` model, add a `Meta` class defining the custom permissions.

- **`views.py`**:  
  For each action (add, edit, delete), use the **`permission_required`** decorator from `django.contrib.auth.decorators` to check the corresponding permission.

- **`urls.py`**:  
  Define URL patterns that use the views decorated with permissions.