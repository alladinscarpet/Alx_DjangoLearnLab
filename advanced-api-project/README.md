### 0. Setting Up a New Django Project with Custom Serializers in Django REST Framework

#### Objective
Initiate a new Django project tailored for advanced API development with Django REST Framework, focusing on creating custom serializers that handle complex data structures and nested relationships.

---

#### Task Description
This task involves setting up a new Django project from scratch, installing Django REST Framework, and configuring a clean environment to develop an API that utilizes custom serializers, including handling nested objects and implementing data validation.

---

#### Steps

1. **Install Django and Django REST Framework**

   - **Action Items:**
     - Install Django and Django REST Framework using pip.
     - In your `advanced-api-project` directory, create a new Django project named **`advanced-api-project`** using the following command:
```bash
       django-admin startproject advanced-api-project
```
       This ensures that Django initializes the project without creating an additional nested folder.
     - Inside the project, create a new Django app named **`api`**.

2. **Configure the Project**

   - **Settings Configuration:**
     - Add **`rest_framework`** to `INSTALLED_APPS` in your project's **`settings.py`**.
     - Ensure the project is set to use Django's default SQLite database for simplicity, or configure another database if preferred.

3. **Define Data Models**

   - **Model Requirements:**
     - Create two models, **`Author`** and **`Book`**.
     - The `Author` model should have the following fields:
       - **`name`**: A string field to store the author's name.
     - The `Book` model should have the following fields:
       - **`title`**: A string field for the book's title.
       - **`publication_year`**: An integer field for the year the book was published.
       - **`author`**: A foreign key linking to the `Author` model, establishing a one-to-many relationship from Author to Books.

   - **Action Items:**
     - Define these models in **`api/models.py`**.
     - Run migrations to create these models in the database.

4. **Create Custom Serializers**

   - **Serializer Details:**
     - Create a **`BookSerializer`** that serializes all fields of the `Book` model.
     - Create an **`AuthorSerializer`** that includes:
       - The `name` field.
       - A nested `BookSerializer` to serialize the related books dynamically.

   - **Validation Requirements:**
     - Add custom validation to the `BookSerializer` to ensure the `publication_year` is not in the future.

5. **Document Your Model and Serializer Setup**

   - **Documentation Requirements:**
     - In the **`models.py`** and **`serializers.py`**, add detailed comments explaining the purpose of each model and serializer.
     - Describe how the relationship between `Author` and `Book` is handled in your serializers.

6. **Implement and Test**

   - **Testing Guidelines:**
     - Use Django admin or the Django shell to manually test creating, retrieving, and serializing `Author` and `Book` instances to ensure your serializers work as expected.
---

---
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

---

---
### 2. Implementing Filtering, Searching, and Ordering in Django REST Framework



#### Objective
Enhance the usability and functionality of your API by implementing filtering, searching, and ordering capabilities.  
This task focuses on providing users with the tools to easily access and manipulate the data presented through your API.

---

#### Task Description
For this task within your **`advanced-api-project`**, you will add advanced query capabilities to your existing views that manage the `Book` model.  
This will allow API consumers to filter, search, and order the books based on different criteria.

---

#### Steps

1. **Set Up Filtering**

   - **Action Items:**
     - Integrate Django REST Framework's filtering capabilities to allow users to filter the book list by various attributes like `title`, `author`, and `publication_year`.
     - Use DRF's **`DjangoFilterBackend`** or similar tools to set up comprehensive filtering options in your `ListView`.

2. **Implement Search Functionality**

   - **Search Setup:**
     - Enable search functionality on one or more fields of the `Book` model, such as `title` and `author`.
     - Configure the **`SearchFilter`** in your API to allow users to perform text searches on these fields.

3. **Configure Ordering**

   - **Ordering Configuration:**
     - Allow users to order the results by any field of the `Book` model, particularly `title` and `publication_year`.
     - Set up the **`OrderingFilter`** to provide front-end flexibility in sorting query results.

4. **Update API Views**

   - **View Modifications:**
     - Adjust your `BookListView` to incorporate filtering, searching, and ordering functionalities.
     - Ensure that these capabilities are clearly defined and integrated into the view logic.

5. **Test API Functionality**

   - **Testing Guidelines:**
     - Test the filtering, searching, and ordering features to ensure they work correctly.
     - Use API testing tools like Postman or curl to make requests with various query parameters to evaluate how the API handles them.

6. **Document the Implementation**

   - **Documentation Requirements:**
     - Detail how filtering, searching, and ordering were implemented in your views.
     - Include examples of how to use these features in API requests in the project documentation or code comments.




---

---


### 3. Writing Unit Tests for Django REST Framework APIs


#### Objective
Develop and execute comprehensive unit tests for your Django REST Framework APIs to ensure the integrity of your endpoints and the correctness of response data and status codes.

---

#### Task Description
In this task within your **`advanced-api-project`**, you will create unit tests for the API endpoints you've developed, focusing on testing their functionality, response data integrity, and status code accuracy.  
This ensures that your API behaves as expected under various conditions and inputs.  
The tests should be written in the **`/api/test_views.py`** file.

---

#### Steps

1. **Understand What to Test**

   - **Identify Key Areas:**
     - Focus on testing CRUD operations for the `Book` model endpoints.
     - Test the filtering, searching, and ordering functionalities to verify they work as intended.
     - Ensure that permissions and authentication mechanisms are correctly enforcing access controls.

2. **Set Up Testing Environment**

   - **Configure Test Settings:**
     - Use Django's built-in test framework which is based on Python's `unittest` module.
     - Configure a separate test database to avoid impacting your production or development data.

3. **Write Test Cases**

   - **Develop Test Scenarios:**
     - Write tests that simulate API requests and check for correct status codes and response data. This includes:
       - Creating a `Book` and ensuring the data is correctly saved and returned.
       - Updating a `Book` and verifying the changes are reflected.
       - Deleting a `Book` and ensuring it is removed from the database.
       - Testing each endpoint with appropriate authentication and permission scenarios to ensure security controls are effective.

4. **Run and Review Tests**

   - **Execute Tests:**
     - Run your test suite using Django's `manage.py` command:
```bash
       python manage.py test api
```
     - Review the outputs and fix any issues or bugs identified by the tests.

5. **Document Your Testing Approach**

   - **Testing Documentation:**
     - Document your testing strategy and individual test cases.
     - Provide guidelines on how to run the tests and interpret test results.