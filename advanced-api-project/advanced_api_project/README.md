### 1. Building Custom Views and Generic Views in Django REST Framework


#### Objective
Learn to construct custom views and utilize generic views in Django REST Framework to handle specific use cases and streamline API development.

---

#### Task Description
Expand your **`advanced-api-project`** by creating and configuring custom views using Django REST Framework's powerful generic views and mixins.  
This task will focus on efficiently handling CRUD operations and fine-tuning API behavior to meet specific requirements.

---

#### Steps

1. **Set Up Generic Views**

   - **Action Items:**
     - Implement a set of generic views for the `Book` model to handle CRUD operations. This includes:
       - A **`ListView`** for retrieving all books.
       - A **`DetailView`** for retrieving a single book by ID.
       - A **`CreateView`** for adding a new book.
       - An **`UpdateView`** for modifying an existing book.
       - A **`DeleteView`** for removing a book.

2. **Define URL Patterns**

   - **Routing Requirements:**
     - Configure URL patterns in **`api/urls.py`** to connect the aforementioned views with specific endpoints.
     - Each view should have a unique URL path corresponding to its function (e.g., `/books/` for the list view, `/books/<int:pk>/` for the detail view).

3. **Customize View Behavior**

   - **Customization Instructions:**
     - Customize the `CreateView` and `UpdateView` to ensure they properly handle form submissions and data validation.
     - Integrate additional functionalities such as permission checks or filters directly into the views using DRF's built-in features or custom methods.

4. **Implement Permissions**

   - **Permissions Setup:**
     - Apply Django REST Framework's permission classes to protect API endpoints based on user roles.
     - For example, restrict `CreateView`, `UpdateView`, and `DeleteView` to authenticated users only, while allowing read-only access to unauthenticated users for `ListView` and `DetailView`.

5. **Test the Views**

   - **Testing Guidelines:**
     - Manually test each view through tools like Postman or curl to ensure they behave as expected. This includes testing the creation, retrieval, update, and deletion of `Book` instances.
     - Confirm that permissions are enforced correctly by attempting to access endpoints with and without proper credentials.

6. **Document the View Configurations**

   - **Documentation Requirements:**
     - Provide clear documentation in your code (via comments) and an external README detailing how each view is configured and intended to operate.
     - Outline any custom settings or hooks used in the views to extend or modify their default behavior.