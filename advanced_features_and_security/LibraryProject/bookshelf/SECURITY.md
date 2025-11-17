## Security Measures Implemented in LibraryProject

This document outlines the security measures applied in the **`LibraryProject`** Django application, covering settings, views, templates, and best practices to prevent common web vulnerabilities.

---

## 1. Secure Django Settings

### **DEBUG=False in Production**
- Prevents sensitive debug information from being exposed to end-users.
```python
DEBUG = False
```

### **Browser XSS Filter**
- Enables the browser's built-in cross-site scripting (XSS) protection.
```python
SECURE_BROWSER_XSS_FILTER = True
```

### **Clickjacking Protection**
- Prevents the site from being embedded in frames.
```python
X_FRAME_OPTIONS = 'DENY'
```

### **MIME Type Sniffing Prevention**
- Ensures browsers respect declared content types.
```python
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### **Cookie Security**
- Ensures cookies are only sent over HTTPS and are HttpOnly.
```python
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
```

---

## 2. CSRF Protection in Templates

All HTML forms include `{% csrf_token %}` to prevent Cross-Site Request Forgery.

**Example:**
```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
    <button type="submit">Submit</button>
</form>
```

---

## 3. Safe Handling of User Input in Views

### **Django ORM Usage**
- Django ORM is used for database queries instead of raw SQL.
- Example of safe search in **`views.py`**:
```python
if form.is_valid():
    query = form.cleaned_data.get("query")
    if query:
        books = books.filter(title__icontains=query)
```

- Prevents SQL injection since the ORM automatically parameterizes queries.
- Form validation sanitizes and cleans input.

### **Form Validation**
- All user-submitted data is validated via Django forms.
- Invalid input is rejected automatically.

---

## 4. Role-Based Access Control (RBAC)

Access to views is restricted based on roles (Admin, Librarian, Member) using:
```python
@user_passes_test(is_admin)
def admin_view(request):
    ...
```

- Only users with the correct role can access sensitive parts of the application.

---

## 5. Permission-Based Access Control

Custom model permissions (**`can_add_book`**, **`can_change_book`**, **`can_delete_book`**) are enforced using:
```python
@permission_required('bookshelf.can_add_book', raise_exception=True)
def add_book(request):
    ...
```

- Only users with the corresponding permission can perform actions like adding, editing, or deleting books.

---

## 6. Content Security Policy (CSP)

Optionally, CSP headers can be applied to restrict which domains can load scripts, styles, and media:
```
Content-Security-Policy: default-src 'self';
```

- This reduces the risk of XSS attacks by only allowing trusted sources.

---

## 7. General Best Practices

### **Password Management**
- Django stores passwords hashed using PBKDF2 by default.

### **HTTPS Enforcement**
- Cookies and sensitive requests are secured with HTTPS.

### **Admin Access**
- Superuser accounts are protected and only accessible by staff with **`is_staff=True`**.

---

## Key Notes

- For maximum security, keep **`DEBUG=False`** in production.
- Always apply migrations after modifying models with permissions or custom user fields.
- Regularly review user roles and permissions to maintain access control integrity.