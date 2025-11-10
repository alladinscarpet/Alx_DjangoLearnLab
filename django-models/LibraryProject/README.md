### 2. Implementing User Authentication in Django


#### Objective
Develop the ability to manage user authentication within a Django application.  
This task focuses on setting up user login, logout, and registration functionalities using Django's built-in authentication system.

---

#### Task Description
Enhance your **`relationship_app`** by adding user authentication features.  
Implement views and templates for user login, logout, and registration to demonstrate how Django manages user sessions and permissions.

---

#### Steps

1. **Setup User Authentication Views**

   - Utilize Django's built-in views and forms for handling user authentication.  
   - You will need to create views for user login, logout, and registration.

2. **Create Templates for Authentication**

   - Provide HTML templates for each authentication action (login, logout, and registration).  
   - Templates will be provided, allowing you to focus on backend integrations.  
   - Below is the recommended templates structure:
```
     relationship_app/
     │── templates/
     │   ├── relationship_app/
     │   │   ├── login.html
     │   │   ├── register.html
     │   │   ├── logout.html
```

3. **Configure URL Patterns**

   - Define URL patterns in **`relationship_app/urls.py`** to link to the authentication views.

4. **Test Authentication Functionality**

   - Ensure that users can register, log in, and log out.

---

**Note:** HTML Templates are provided.