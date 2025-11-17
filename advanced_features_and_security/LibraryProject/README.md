### 1. Managing Permissions and Groups in Django

#### Objective
Implement and manage permissions and groups to control access to various parts of your Django application, enhancing security and functionality.

---

#### Task Description
Develop a system within your Django application that utilizes groups and permissions to restrict access to certain parts of your application.  
This task will demonstrate your ability to set up detailed access controls based on user roles and their assigned permissions.

---

#### Steps

1. **Define Custom Permissions in Models**

   Add custom permissions to one of your existing models (or a new model if preferable) to control actions such as viewing, creating, editing, or deleting instances of that model.

   - **Model Permissions to Add:**
     - Create permissions such as **`can_view`**, **`can_create`**, **`can_edit`**, and **`can_delete`** within your chosen model.

2. **Create and Configure Groups with Assigned Permissions**

   Set up user groups in Django and assign the newly created permissions to these groups.  
   Use Django's admin site to manage these groups and their permissions.

   - **Groups to Setup:**
     - Create groups like **`Editors`**, **`Viewers`**, and **`Admins`**.
     - Assign appropriate permissions to each group. For example, `Editors` might have `can_edit` and `can_create` permissions.

3. **Enforce Permissions in Views**

   Modify your views to check for these permissions before allowing users to perform certain actions.  
   Use decorators such as **`permission_required`** to enforce these permissions in your views.

   - **Views to Modify or Create:**
     - Ensure views that create, edit, or delete model instances check for the correct permissions.
     - **Example:** Use `@permission_required('app_name.can_edit', raise_exception=True)` to protect an edit view.

4. **Test Permissions**

   Manually test the implementation by assigning different users to groups and verifying that the permissions are enforced correctly.

   - **Testing Approach:**
     - Create test users and assign them to different groups.
     - Log in as these users and attempt to access various parts of the application to ensure that permissions are applied correctly.

5. **Document the Setup**

   - Provide a concise guide or notes within your code on how the permissions and groups are set up and used in the application.
   - This could be in the form of comments or a simple README file.
   - Make sure to use the variable name as defined above such as **`can_edit`**, **`can_create`**.

---

#### Deliverables

1. **`models.py`**: Updated with custom permissions for at least one model.
2. **`views.py`**: Updated to include permission checks in relevant views.
3. **Documentation**: Comments or a README file explaining how permissions and groups are configured and used.