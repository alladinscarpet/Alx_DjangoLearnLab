### 0. Introduction to Django Development Environment Setup

**Mandatory**

#### Objective
Gain familiarity with Django by setting up a Django development environment and creating a basic Django project.  
This task aims to introduce you to the workflow of Django projects, including project creation and running the development server.

---

#### Task Description
Install Django and create a new Django project named **LibraryProject**.  
This initial setup will serve as the foundation for developing Django applications.  
You’ll also explore the project’s default structure to understand the roles of various components.

---

#### Steps

1. **Install Django**

   - Ensure **Python** is installed on your system.  
   - Install Django using **pip**:  
     ```bash
     pip install django
     ```

2. **Create Your Django Project**

   - Create a new Django project by running:  
     ```bash
     django-admin startproject LibraryProject
     ```
   - This will create a new folder named **LibraryProject** containing the initial Django setup.

3. **Run the Development Server**

   - Navigate into your project directory:  
     ```bash
     cd LibraryProject
     ```
   - Create a `README.md` file inside the **LibraryProject** folder (you’re reading it now!).  
   - Start the development server using:  
     ```bash
     python manage.py runserver
     ```
   - Open a web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the default Django welcome page confirming that your setup was successful.

4. **Explore the Project Structure**

   Familiarize yourself with the created project structure. Pay particular attention to:

   - **`settings.py`** – Configuration for the Django project.  
   - **`urls.py`** – The URL declarations for the project; acts as the “table of contents” for your Django-powered site.  
   - **`manage.py`** – A command-line utility that lets you interact with this Django project (e.g., starting the server, creating apps, applying migrations).
