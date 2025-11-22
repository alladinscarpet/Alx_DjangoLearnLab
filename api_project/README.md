### 0. Setting Up a New Django Project with Django REST Framework



#### Objective
Begin your journey with Django REST Framework by setting up a new Django project from scratch, specifically for building APIs.  
This task will introduce you to the initial steps necessary to integrate DRF and prepare for creating API endpoints.

---

#### Task Description
In this task, you will create a new Django project, configure Django REST Framework, and prepare the environment for future tasks focused on building APIs.

---

#### Steps

1. **Create a New Django Project**

   Start by setting up a new Django project dedicated to API development.

   - **Installation and Project Creation:**
     - If not already installed, install Django using:
```bash
       pip install django
```
     - Create a new Django project named **`api_project`** by running:
```bash
       django-admin startproject api_project
```

2. **Install Django REST Framework**

   Add Django REST Framework to your new project to facilitate API development.

   - **Install DRF:**
     - Run the following command to install the framework:
```bash
       pip install djangorestframework
```
     - Add **`'rest_framework'`** to the `INSTALLED_APPS` in the **`settings.py`** of your `api_project`.

3. **Create a New Django App**

   Set up an app within your project that will be specifically used for handling API logic.

   - **Create App:**
     - Inside the `api_project` directory, run:
```bash
       python manage.py startapp api
```
     - Add **`'api'`** to the `INSTALLED_APPS` in **`settings.py`**.

4. **Define a Simple Model**

   Create a model to be used for your first API. This model will be simple, designed to be easily understood and used in an API.

   - **Example Model:**
     - In **`api/models.py`**, define a `Book` model with basic fields such as:
       - **`title`**: A CharField
       - **`author`**: A CharField

5. **Run Migrations**

   Set up your database tables based on the new models created.

   - **Migrate Database:**
     - Run the following commands to create and apply migrations:
```bash
       python manage.py makemigrations
       python manage.py migrate
```

6. **Start the Development Server**

   Ensure that your setup is correct by running the Django development server.

   - **Start Server:**
     - Use the following command to start the server:
```bash
       python manage.py runserver
```
     - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to confirm the server is running correctly.