### 3. Implementing Authentication and Permissions in Django REST Framework

#### Objective
Secure your API endpoints by implementing various authentication schemes and permission settings in Django REST Framework.  
This task will ensure that only authorized users can access and modify data through your API.

---

#### Task Description
For this task within your **`api_project`**, you will add authentication and permission layers to your existing API endpoints.  
This will involve configuring DRF to use token authentication and setting up permission classes to restrict access based on user roles or authentication status.

---

#### Steps

1. **Configure Authentication**

   Set up token authentication in DRF, allowing your API to handle and verify tokens for authenticated requests.

   - **Install and Configure Authentication:**
     - If not already included, add **`rest_framework.authtoken`** to your `INSTALLED_APPS` in **`settings.py`**.
     - Run the following command to create the necessary database tables for token management:
```bash
       python manage.py migrate
```
     - Update your DRF settings in **`settings.py`** to include token authentication in the `DEFAULT_AUTHENTICATION_CLASSES`.

2. **Generate and Use Tokens**

   Provide a way for users to obtain a token and use it for authenticated requests.

   - **Token Retrieval Endpoint:**
     - Implement a view that allows users to obtain a token by providing their username and password.
     - This can be done using DRF's built-in views like **`obtain_auth_token`**.

3. **Define Permission Classes**

   Control who can access your API views based on permissions. Define custom permission classes or use DRF's built-in permissions to restrict access.

   - **Set Up Permissions:**
     - Use `rest_framework.permissions` to apply basic permissions like **`IsAuthenticated`**, **`IsAdminUser`**, or custom permissions based on your application's needs.
     - Modify your `ViewSet` configurations to include the appropriate permissions.

4. **Test Authentication and Permissions**

   Verify that your API endpoints are secure by testing with and without authentication tokens, and check the behavior based on different user permissions.

   - **Testing Authentication:**
     - Use tools like Postman or curl to send requests with and without the token to see if the permissions are enforced correctly.

5. **Document the Authentication and Permission Setup**

   Provide documentation or comments in your code explaining how authentication and permissions are configured and how they work in your API setup.

---

#### Deliverables

1. **Updated `settings.py`**: Include token authentication in the REST framework settings.
2. **Authentication Views**: Implement or enable views for token retrieval.
3. **`views.py`**: Update viewsets with permission classes.