# API View Configuration Steps

## Step 1 — Create Generic Views for the Book Model

**File:** `api/views.py`

### Actions:

1. **BookListView (`ListAPIView`)**
   - Retrieves all book instances (`GET api/books/`)
   - **Permission:** public (`AllowAny`)
   - Standard DRF behavior, no extra hooks.

2. **BookDetailView (`RetrieveAPIView`)**
   - Retrieves a single book by ID (`GET api/books/<int:pk>/`)
   - **Permission:** public (`AllowAny`)
   - Standard DRF behavior.

3. **BookCreateView (`CreateAPIView`)**
   - Creates a new book (`POST api/books/create/`)
   - **Permission:** admin-only for write (`IsAdminOrReadOnly`)
   - **Custom hook:** `perform_create()` — capitalizes the title and allows additional logic (e.g., tagging creator, sanitizing input).

4. **BookUpdateView (`UpdateAPIView`)**
   - Updates an existing book (`PUT/PATCH api/books/<int:pk>/update/`)
   - **Permission:** admin-only for write (`IsAdminOrReadOnly`)
   - **Custom hook:** `perform_update()` — currently saves data as-is; place to add update-specific logic.

5. **BookDeleteView (`DestroyAPIView`)**
   - Deletes a book (`DELETE api/books/<int:pk>/delete/`)
   - **Permission:** admin-only for write (`IsAdminOrReadOnly`)
   - Standard DRF destroy behavior.

### Additional Setup:

- **`permissions.py`** → defined `IsAdminOrReadOnly` custom class: read-only for everyone, write only for admin users.

---

## Step 2 — Add URL Patterns

**File:** `api/urls.py`

### Actions:

1. Map each view to a clear endpoint:
   - `api/books/` → list all books
   - `api/books/<int:pk>/` → retrieve single book
   - `api/books/create/` → create book
   - `api/books/<int:pk>/update/` → update book
   - `api/books/<int:pk>/delete/` → delete book

2. Ensures endpoints are RESTful and correspond directly to CRUD operations.

3. URLs allow clients and tools like Postman to access each view and verify permissions.

---

## Summary of Custom Behavior

- **Hooks:** `perform_create()` and `perform_update()` allow modification of incoming data before saving.
- **Permissions:** `IsAdminOrReadOnly` enforces role-based access.
- **Views:** Generic DRF views handle most CRUD logic automatically.
- **URLs:** Structured so that read and write endpoints are clearly separated.