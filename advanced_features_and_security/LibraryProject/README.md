### 0. Implementing a Custom User Model in Django 



#### Objective
Customize Django's user model in bookshelf app to suit the specific needs of your application, demonstrating an understanding of extending Django's authentication system.

---

#### Task Description
For this task, you will replace Django's default user model with a custom user model that includes additional fields and functionality.  
This is a critical feature for applications that require user attributes beyond Django's built-in user model.

---

#### Steps

1. **Set Up the Custom User Model**

   - Duplicate the previous Django project directory **`django-models`** and rename it to **`advanced_features_and_security`**.
   - Create a custom user model by extending **`AbstractUser`**, adding custom fields that are relevant to your application's needs.

   - **Fields to Add:**
     - **`date_of_birth`**: A date field.
     - **`profile_photo`**: An image field.

2. **Update Settings to Use the Custom User Model**

   Configure Django to use this custom user model for all user-related functionalities.

   - **Settings Configuration:**
     - In your project's **`settings.py`**, set the **`AUTH_USER_MODEL`** to point to your new custom user model.

3. **Create User Manager for Custom User Model**

   Implement a custom user manager that handles user creation and queries, ensuring it can manage the added fields effectively.

   - **Custom Manager Functions to Implement:**
     - **`create_user`**: Ensure it handles the new fields correctly.
     - **`create_superuser`**: Ensure administrative users can still be created with the required fields.

4. **Integrate the Custom User Model into Admin**

   Modify the Django admin to support the custom user model, ensuring that administrators can manage users effectively through the Django admin interface.

   - **Admin Modifications Required:**
     - Define a custom **`ModelAdmin`** class that includes configurations for the additional fields in your user model.

5. **Update Your Application to Use the Custom User Model**

   Adjust any part of your application that references the user model to use the new custom model.

   - **Application Updates:**
     - Update all foreign keys or user model references in your other models to use the custom user model.

---

#### Deliverables

1. **`models.py`**: Include your custom user model and custom user manager.
2. **`admin.py`**: Set up the admin interface to manage the custom user model effectively.
3. **`settings.py`**: Modify to specify the custom user model as the default for the project.