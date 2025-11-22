# Authentication and Permissions in DRF API

## Step 1 — Enable Token Authentication

**Objective:** Ensure that only users with valid credentials can access protected API endpoints.

### Actions Taken:

1. **Add the token app in `settings.py`:**
```python
   INSTALLED_APPS = [
       ...
       'rest_framework',
       'rest_framework.authtoken',  # Enables token authentication
       'api',
   ]
```

2. **Create database tables for tokens:**
```bash
   python manage.py migrate
```

   Creates the `authtoken_token` table to store tokens for existing users.

3. **Set DRF defaults in `settings.py`:**
```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.TokenAuthentication',
       ],
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ]
   }
```

### Explanation:

- **`TokenAuthentication`**: DRF checks the `Authorization` header for a token in the form `Token <your_token>`.
- **`IsAuthenticated`**: Only users with a valid token can access endpoints globally (unless overridden per view).

---

## Step 2 — Create a Token Login Endpoint

**Objective:** Allow users to obtain a token with their username and password.

### Implementation:

In **`api_project/urls.py`**:
```python
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    ...
    path('api/token/', obtain_auth_token),  # Users POST here to get their token
]
```

### Usage:

Send a **POST** request:
```http
POST /api/token/
{
    "username": "userx",
    "password": "12345"
}
```

### Response:
```json
{
    "token": "asdj83h3d92jd92jdh2..."
}
```

Use the token in all future requests:
```
Authorization: Token asdj83h3d92jd92jdh2...
```

---

## Step 3 — Add Permissions to Your API

Permissions control what users can do once authenticated.



### Option A — Enforce Token-Based Authentication

Apply per view/viewset:
```python
permission_classes = [IsAuthenticated]
```

**Effect:**
- Only users with a valid token can access the endpoint.
- All authenticated users can read and write (GET, POST, PUT, DELETE).
- **Example:** `BookViewSet` will allow CRUD operations only if the token is valid.

---

### Option B — Custom Permission Class

Create **`permissions.py`**:
```python
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Read-only for anyone, write only for admin users.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # GET, HEAD, OPTIONS allowed
        return request.user and request.user.is_staff  # POST, PUT, DELETE only for admin
```

Apply per view/viewset:
```python
permission_classes = [IsAdminOrReadOnly]
```

**Effect:**
- **GET, HEAD, OPTIONS** → accessible to everyone (even without a token if global defaults are not enforced).
- **POST, PUT, DELETE** → only admin users can modify data.
- Tokens are only required if global authentication defaults are in place or overridden.

**Important:**
- The file `permissions.py` alone does nothing.
- What matters is how you apply the custom permission using `permission_classes` in the view or viewset.
- This allows fine-grained control per endpoint.

---

## Overall Flow in Our API and Request Handling in DRF

When a client makes a request to the API:

### 1. Authentication (Token Check)

DRF checks the token first, because you enabled `TokenAuthentication` globally in `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

The client sends the token in the `Authorization` header:
```
Authorization: Token <user_token>
```

DRF verifies:
- The token exists in the `authtoken_token` table.
- The token is associated with a valid user.

If the token is **missing or invalid** → **401 Unauthorized** → request stops here.

**Scope:**
- Each token is user-specific (one token per user unless multiple are generated).
- It represents the identity of that user for the duration of the request.
- While valid, DRF knows exactly which user is making the request.

---

### 2. Permission Check

After successful authentication, DRF checks permissions, which determine what the user can do.

#### Option A (`permission_classes = [IsAuthenticated]`)

- Enforces token-based authentication per view/viewset.
- Only users with a valid token can access the endpoint.
- **No token** → **401 Unauthorized**.
- **Valid token** → allowed to perform all actions allowed by the view/viewset.

#### Option B (`permission_classes = [IsAdminOrReadOnly]`)

- Uses a custom permission class.
- DRF still checks the token (because `TokenAuthentication` is global), but now permissions are granular:
  - **Read-only methods (GET, HEAD, OPTIONS)** → allowed for everyone, even without a token.
  - **Write methods (POST, PUT, DELETE)** → only allowed for admin users.
- Attempting a restricted action → **403 Forbidden**.

**Key Concept:**
- **Authentication first** → *"Is this user who they claim to be?"* → controlled by the token.
- **Permission second** → *"What is this user allowed to do?"* → controlled by `permission_classes`.

Think of it as **two layers of security**:
- **Token** → Identity
- **Permission** → Access rights

---

### 3. View Logic Execution

Only if both authentication and permissions pass, the request reaches your view/viewset.

**Example:** `BookViewSet` will allow CRUD operations depending on the user's permissions.