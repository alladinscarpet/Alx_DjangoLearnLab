# Social Media API Documentation

## Base URL
`http://127.0.0.1:8000/api/`

## Authentication

Uses **Token Authentication**.
Mental model: Office badge stored at reception such that every time you enter, security checks your badge against the system

Include the token in the header for authenticated requests:
```
Authorization: Token <your_token_here>
```

---

## 1. User Endpoints

### 1.1 Register User

**Endpoint:** `/api/register/`  
**Method:** `POST`  
**Description:** Create a new user and return an authentication token.  
**Auth Required:** No

#### Request Body:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword",
  "bio": "Hello, I am John!"
}
```

#### Response (201 Created):
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "bio": "Hello, I am John!",
  "token": "abc123def456"
}
```

#### Error (400 Bad Request if username exists):
```json
{
  "username": ["This username is already taken."]
}
```

---

### 1.2 Login User

**Endpoint:** `/api/login/`  
**Method:** `POST`  
**Description:** Authenticate user and return a token.  
**Auth Required:** No

#### Request Body:
```json
{
  "username": "john_doe",
  "password": "securepassword"
}
```

#### Response (200 OK):
```json
{
  "token": "abc123def456"
}
```

#### Error (400 Bad Request if credentials invalid):
```json
{
  "error": "Invalid credentials"
}
```

---

## 2. Posts Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/posts/` | GET | List all posts | Optional |
| `/api/posts/` | POST | Create post | Yes |
| `/api/posts/<id>/` | GET | Retrieve post | Optional |
| `/api/posts/<id>/` | PUT/PATCH | Update post | Yes, author only |
| `/api/posts/<id>/` | DELETE | Delete post | Yes, author only |

---

### 2.1 List Posts

**Endpoint:** `/api/posts/`  
**Method:** `GET`  
**Description:** Get a list of all posts.

#### Request (optional token in header):
```
GET /api/posts/
```

#### Response (200 OK):
```json
[
  {
    "id": 1,
    "author": "john_doe",
    "title": "My First Post",
    "content": "Hello world!",
    "created_at": "2025-12-22T12:00:00Z",
    "updated_at": "2025-12-22T12:00:00Z"
  },
  {
    "id": 2,
    "author": "alice",
    "title": "Travel Plans",
    "content": "Visiting Kenya next week!",
    "created_at": "2025-12-21T09:30:00Z",
    "updated_at": "2025-12-21T09:30:00Z"
  }
]
```

---

### 2.2 Create Post

**Endpoint:** `/api/posts/`  
**Method:** `POST`  
**Description:** Create a new post.  
**Auth Required:** Yes

#### Request Header:
```
Authorization: Token abc123def456
```

#### Request Body:
```json
{
  "title": "New Adventures",
  "content": "Excited to share my journey!"
}
```

#### Response (201 Created):
```json
{
  "id": 3,
  "author": "john_doe",
  "title": "New Adventures",
  "content": "Excited to share my journey!",
  "created_at": "2025-12-22T14:00:00Z",
  "updated_at": "2025-12-22T14:00:00Z"
}
```

#### Error (401 Unauthorized if no token):
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 2.3 Retrieve Single Post

**Endpoint:** `/api/posts/<id>/`  
**Method:** `GET`  
**Description:** Retrieve a specific post by ID.  
**Auth Required:** Optional

#### Request:
```
GET /api/posts/3/
```

#### Response (200 OK):
```json
{
  "id": 3,
  "author": "john_doe",
  "title": "New Adventures",
  "content": "Excited to share my journey!",
  "created_at": "2025-12-22T14:00:00Z",
  "updated_at": "2025-12-22T14:00:00Z"
}
```

---

### 2.4 Update Post

**Endpoint:** `/api/posts/<id>/`  
**Method:** `PUT` / `PATCH`  
**Description:** Update a post. Only the author can update.  
**Auth Required:** Yes

#### Request Header:
```
Authorization: Token abc123def456
```

#### Request Body:
```json
{
  "title": "Updated Adventures",
  "content": "I have new experiences!"
}
```

#### Response (200 OK):
```json
{
  "id": 3,
  "author": "john_doe",
  "title": "Updated Adventures",
  "content": "I have new experiences!",
  "created_at": "2025-12-22T14:00:00Z",
  "updated_at": "2025-12-22T15:00:00Z"
}
```

#### Error (403 Forbidden if not author):
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 2.5 Delete Post

**Endpoint:** `/api/posts/<id>/`  
**Method:** `DELETE`  
**Description:** Delete a post. Only the author can delete.  
**Auth Required:** Yes

#### Request Header:
```
Authorization: Token abc123def456
```

#### Response (204 No Content):
```
No content
```

#### Error (403 Forbidden if not author):
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## 3. Comments Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/comments/` | GET | List comments | Optional |
| `/api/comments/` | POST | Create comment | Yes |
| `/api/comments/<id>/` | PUT/PATCH | Update comment | Yes, author only |
| `/api/comments/<id>/` | DELETE | Delete comment | Yes, author only |

---

### 3.1 List Comments

**Endpoint:** `/api/comments/`  
**Method:** `GET`

#### Response (200 OK):
```json
[
  {
    "id": 1,
    "post": 3,
    "author": "alice",
    "content": "Great post!",
    "created_at": "2025-12-22T14:30:00Z",
    "updated_at": "2025-12-22T14:30:00Z"
  }
]
```

---

### 3.2 Create Comment

**Endpoint:** `/api/comments/`  
**Method:** `POST`  
**Auth Required:** Yes

#### Request Header:
```
Authorization: Token abc123def456
```

#### Request Body:
```json
{
  "post": 3,
  "content": "This is awesome!"
}
```

#### Response (201 Created):
```json
{
  "id": 2,
  "post": 3,
  "author": "john_doe",
  "content": "This is awesome!",
  "created_at": "2025-12-22T15:00:00Z",
  "updated_at": "2025-12-22T15:00:00Z"
}
```

---

### 3.3 Update Comment

**Endpoint:** `/api/comments/<id>/`  
**Method:** `PUT` / `PATCH`  
**Auth Required:** Yes, only author

#### Request Body:
```json
{
  "content": "Updated comment text!"
}
```

#### Response (200 OK):
```json
{
  "id": 2,
  "post": 3,
  "author": "john_doe",
  "content": "Updated comment text!",
  "created_at": "2025-12-22T15:00:00Z",
  "updated_at": "2025-12-22T15:15:00Z"
}
```

#### Error (403 Forbidden if not author):
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 3.4 Delete Comment

**Endpoint:** `/api/comments/<id>/`  
**Method:** `DELETE`  
**Auth Required:** Yes, only author

#### Response (204 No Content):
```
No content
```

#### Error (403 Forbidden if not author):
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Notes:

- All create/update/delete operations require **Token authentication**.
- Listing posts/comments is open to anyone.
- Author-only restrictions are enforced via the `IsAuthorOrReadOnly` custom permission.
- Dates are in ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`).
- Use the `Authorization: Token <token>` header for authenticated requests.