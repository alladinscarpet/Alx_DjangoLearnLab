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