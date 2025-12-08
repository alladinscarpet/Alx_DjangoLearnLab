### 0. Initial Setup and Project Configuration for a Django Blog


#### Objective
Set up a new Django project specifically for a blog, which includes configuring the environment, establishing the initial models, and preparing the base templates.  
This foundational task ensures all participants start with a consistent and standardized setup.

---

#### Task Description
Kick off the development of a comprehensive Django blog project.  
You'll begin by setting up the Django environment, creating the primary Django application, and configuring the basic models necessary for a blogging platform.

---

#### Steps

1. **Project Setup**

   - **Install Django and Start the Project:**
     - Ensure Django is installed using:
```bash
       pip install django
```
     - Create a new Django project named **`django_blog`**:
```bash
       django-admin startproject django_blog
```
     - Navigate into your project directory and create a new Django app called **`blog`**:
```bash
       cd django_blog
       python manage.py startapp blog
```
     - Register the new `blog` app by adding it to the `INSTALLED_APPS` list in **`django_blog/settings.py`**.

2. **Configure the Database**

   - **Database Configuration:**
     - By default, Django uses SQLite. If this is sufficient for your blog, no action is needed.
     - However, for learning purposes, you can configure it to use PostgreSQL or another database by adjusting the `DATABASES` setting in **`settings.py`**.

3. **Define Blog Models**

   - **Model Specifications:**
     - Create a model **`Post`** in **`blog/models.py`** with the following fields:
       - **`title`**: `models.CharField(max_length=200)`
       - **`content`**: `models.TextField()`
       - **`published_date`**: `models.DateTimeField(auto_now_add=True)`
       - **`author`**: `models.ForeignKey` to Django's `User` model, with a relation to handle multiple posts by a single author.
     - Run the migrations to create the model in the database:
```bash
       python manage.py makemigrations blog
       python manage.py migrate
```

4. **Set Up Static and Template Directories**

   - **Static Files and Templates:**
     - Create directories for static files and templates within the `blog` app.
     - Place the provided HTML, CSS, and JavaScript files into the appropriate directories.
     - Ensure that Django is configured to find these files by setting `STATIC_URL` and `TEMPLATES` in **`settings.py`**.

5. **Launch the Development Server**

   - **Initial Testing:**
     - Start the Django development server to ensure everything is set up correctly:
```bash
       python manage.py runserver
```
     - Open a browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to see the initial setup.

---

#### Deliverables

1. **Project Structure**: Submit the entire Django project setup, including settings and initial migrations.
2. **Code Files**: Include your **`models.py`** with the `Post` model defined.
3. **Static and Template Files**: Provide all HTML, CSS, and JavaScript files correctly placed in their respective directories.