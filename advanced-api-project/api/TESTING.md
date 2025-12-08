# API Testing Documentation — Book Endpoints

## Objective

Ensure that all API endpoints for the Book model work correctly, return expected status codes, enforce permissions, and support filtering, searching, and ordering.

---

## Step 1 — Understand What to Test

Before writing tests, we manually verify the API behavior. This acts as a checklist for expected outcomes.

### 1A — CRUD Endpoints

| Operation | URL | Expected Response | Notes |
|-----------|-----|-------------------|-------|
| List Books | `GET /api/books/` | 200 OK, returns a list of all books | Public access (`permission_classes = AllowAny`) |
| Create Book | `POST /api/books/create/` | 201 Created for admin users, 403 Forbidden or "Authentication credentials were not provided." for anonymous users | Uses `IsAdminOrReadOnly` |
| Retrieve Single Book | `GET /api/books/<id>/` | 200 OK, returns book data | Public access |
| Update Book | `PUT /api/books/update/<id>/` | 200 OK for admin users, 403 Forbidden for non-admin | Uses `IsAdminOrReadOnly` |
| Delete Book | `DELETE /api/books/delete/<id>/` | 204 No Content for admin, 403 Forbidden for non-admin | Uses `IsAdminOrReadOnly` |

**Example links:**

- List Books: http://127.0.0.1:8000/api/books/
- Create Book: http://127.0.0.1:8000/api/books/create/
- Update Book: http://127.0.0.1:8000/api/books/update/4
- Delete Book: http://127.0.0.1:8000/api/books/delete/4
- Retrieve Book: http://127.0.0.1:8000/api/books/4

### 1B — Filtering / Search / Ordering

| Feature | Example URL | Expected Response | Notes |
|---------|-------------|-------------------|-------|
| Filter by title | `/api/books/?title=Frozen` | List of books with title "Frozen" | Case-insensitive if using `icontains` |
| Filter by author | `/api/books/?author__name=Rowling` | List of books by author containing "Rowling" | Nested field filtering |
| Search | `/api/books/?search=Frozen` | Returns books whose title or author matches "Frozen" | Uses `search_fields` in view |
| Ordering | `/api/books/?ordering=publication_year` | Books ordered ascending by `publication_year` | Default ordering can be overridden with `ordering` query |

---

## Step 2 — Set Up Testing Environment

### Create test file

Inside `api/`, create: **`api/test_views.py`**.

### Import required tools
```python
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Book, Author
from django.contrib.auth.models import User
```

### Django handles database automatically

- Creates a temporary test database
- Runs all tests inside it
- Deletes it afterward

### Django conventions for discovery

- Test file names must start with `test` (e.g., `test_views.py`)
- Test methods must start with `test_` to be executed automatically
- Running `python manage.py test api` executes all `test*.py` files inside the `api` app

---

## Step 3 — Write Test Cases

Within `BookAPITests(APITestCase)`:

### A. setUp(self)

```python
# method to create author, books, and a user.
def setUp(self):
    self.user = User.objects.create_user(username='test', password='pass123')
    # to enable user to be an admin
    self.user.is_staff = True
    self.user.save()  # Persist is_staff to DB

    self.author = Author.objects.create(name="J.K. Rowling")
    self.book = Book.objects.create(
        title="Harry Potter 1",
        publication_year=1997,
        author=self.author
    )
    # Log in the test client so all requests are authenticated
    self.client.login(username='test', password='pass123')
```

- Creates a test user, marks as admin (`is_staff=True`), and saves it
- Creates a sample author and book
- Logs in client: `self.client.login(...)`

**Why:** Provides consistent test data and authenticated requests for each test method.

### B. Test Book List API
```python
def test_list_books(self):
    url = reverse('book-list')  # GET /api/books/
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
```

**What it does:** Ensures the list endpoint returns all books with 200 OK.  
**Why:** Validates public access and correct serialization of multiple objects.

### C. Test Create Book
```python
def test_create_book(self):
    url = reverse('book-create')  # POST /api/books/create/
    data = {'title': 'New Book', 'publication_year': 2020, 'author': self.author.id}
    response = self.client.post(url, data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Book.objects.count(), 2)
```

**What it does:** Confirms admin users can create books successfully.  
**Why:** Validates `IsAdminOrReadOnly` permission and that database is updated.

**Non-admin behavior:** POST as anonymous → 403 Forbidden

### D. Test Retrieve Single Book
```python
def test_retrieve_book(self):
    url = reverse('book-detail', args=[self.book.id])  # GET /api/books/<id>/
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
```

**What it does:** Ensures single book retrieval works.  
**Why:** Confirms correct mapping of URL → View → Serializer.

### E. Test Update Book
```python
def test_update_book(self):
    url = reverse('book-update', args=[self.book.id])  # PUT /api/books/update/<id>/
    data = {'title': 'Updated Title', 'author': self.author.id, 'publication_year': 1997}
    response = self.client.put(url, data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.book.refresh_from_db()
    self.assertEqual(self.book.title, "Updated Title")
```

**What it does:** Verifies updating book fields works for admin users.  
**Non-admin behavior:** Returns 403 Forbidden.

### F. Test Delete Book
```python
def test_delete_book(self):
    url = reverse('book-delete', args=[self.book.id])  # DELETE /api/books/delete/<id>/
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Book.objects.count(), 0)
```

**What it does:** Confirms admin users can delete a book.  
**Non-admin behavior:** Returns 403 Forbidden.

### G. Test Filter by Title
```python
def test_filter_by_title(self):
    url = reverse('book-list') + "?title__icontains=harry"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
```

**What it does:** Validates that filtering by title works correctly.

### H. Test Search
```python
def test_search(self):
    url = reverse('book-list') + "?search=harry"
    response = self.client.get(url)
    self.assertEqual(len(response.data), 1)
```

**What it does:** Ensures search queries on title or author return correct results.

### I. Test Ordering
```python
def test_ordering(self):
    Book.objects.create(title="A Book", publication_year=1990, author=self.author)
    url = reverse('book-list') + "?ordering=publication_year"
    response = self.client.get(url)
    years = [b['publication_year'] for b in response.data]
    self.assertEqual(years, sorted(years))
```

**What it does:** Confirms ordering by any allowed field works as expected.

---

## Step 4 — Run and Review Tests

Run all tests for the `api` app:
```bash
python manage.py test api
```

### What happens:

- Django creates a temporary database
- Runs all `test*.py` files inside `api/`
- Executes every method starting with `test_`
- Displays pass/fail results
- Destroys the test database afterward

### Interpreting results:

- **OK** → all endpoints behave as expected
- **FAIL** → indicates a mismatch in expected behavior, such as permissions or incorrect response