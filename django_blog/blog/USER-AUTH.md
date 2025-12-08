# User Authentication Documentation — Django Blog

## 1 — Settings Configuration

In **`django_blog/settings.py`**, you configure the Django authentication system and messaging:
```python
INSTALLED_APPS += [
    'django.contrib.auth',      # Django's built-in authentication system
    'django.contrib.messages',  # Enables displaying messages (success/error)
    'blog',                     # Your blog app
]

MIDDLEWARE += [
    'django.contrib.sessions.middleware.SessionMiddleware',  # Handles session management
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Adds request.user
    'django.contrib.messages.middleware.MessageMiddleware',   # Enables messages
]

LOGIN_REDIRECT_URL = 'index'   # Where users go after login
LOGOUT_REDIRECT_URL = 'login'  # Where users go after logout
LOGIN_URL = 'login'            # Where @login_required redirects anonymous users
```

**Why:** This ensures the authentication system works, messages can be shown, and users are redirected properly after login/logout.

---

## 2 — Forms

In **`blog/forms.py`** you created:

### RegisterForm
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
```

**What it does:** Adds email to default user creation form.

**Why:** Default `UserCreationForm` doesn't include email; email is commonly required.

### ProfileForm
```python
from django import forms
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
```

**What it does:** Lets a logged-in user edit username and email.

**Why:** Provides a simple profile management interface.

---

## 3 — Views

In **`blog/views.py`**:

### Index View
```python
from django.shortcuts import render
from .models import Post

def index(request):
    latest_posts = Post.objects.order_by('-published_date')[:5]
    return render(request, "blog/index.html", {"latest_posts": latest_posts})
```

**What it does:** Shows landing page with latest 5 posts.

**Why:** Entry point for all users; introduces the blog content.

### Register View
```python
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("index")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})
```

**What it does:** Handles registration, logs in user, shows success/error messages.

**Why:** Streamlines user onboarding.

### Profile View
```python
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("blog:profile")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "blog/profile.html", {"form": form})
```

**What it does:** Lets authenticated users edit profile.

**Why:** Protects profile page and ensures only logged-in users can update info.

---

## 4 — URLs Configuration

In **`blog/urls.py`**:
```python
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Home page

    # Authentication
    path('login/',  LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path("profile/", views.profile_view, name="profile")
]
```

**What it does:** Connects views to URLs, including built-in login/logout.

**Why:** Provides clean and secure routing for authentication pages.

---

## 5 — Templates

All templates are in **`blog/templates/blog/`**:

### base.html
```django
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Django Blog{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'blog/css/styles.css' %}">
    <script src="{% static 'blog/js/scripts.js' %}"></script>
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="{% url 'index' %}">Home</a></li>
                {% if user.is_authenticated %}
                    <li><a href="{% url 'logout' %}">Logout</a></li>
                    <li><a href="{% url 'profile' %}">Profile</a></li>
                {% else %}
                    <li><a href="{% url 'login' %}">Login</a></li>
                    <li><a href="{% url 'register' %}">Register</a></li>
                {% endif %}
            </ul>
        </nav>
    </header>

    {% if messages %}
      {% for message in messages %}
        <p class="message">{{ message }}</p>
      {% endfor %}
    {% endif %}

    <main>{% block content %}{% endblock %}</main>
</body>
</html>
```

**Purpose:** Base template for all pages, loads CSS/JS, header nav, and global messages.

### index.html
```django
{% extends "blog/base.html" %}
{% block title %}Home - Django Blog{% endblock %}
{% block content %}
<h2>{% if user.is_authenticated %}Welcome back, {{ user.username }}!{% else %}Welcome to the Django Blog!{% endif %}</h2>
<p>Discover amazing posts.</p>
<ul>
    {% for post in latest_posts %}
        <li>{{ post.title }} by {{ post.author }}</li>
    {% endfor %}
</ul>
{% endblock %}
```

**Purpose:** Landing page with latest posts and a personalized welcome message.

### register.html
```django
{% extends "blog/base.html" %}
{% block title %}Register{% endblock %}
{% block content %}
<h1>Register</h1>
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Register</button>
</form>
<p>Already have an account? <a href="{% url 'login' %}">Login</a></p>
{% endblock %}
```

**Purpose:** Registration page with CSRF protection and form rendering.

### login.html
```django
{% extends "blog/base.html" %}
{% block title %}Login{% endblock %}
{% block content %}
<h1>Login</h1>
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
</form>
<p>Don't have an account? <a href="{% url 'register' %}">Register</a></p>
{% endblock %}
```

**Purpose:** Login page, uses Django's built-in login form.

### profile.html
```django
{% extends "blog/base.html" %}
{% block title %}Profile{% endblock %}
{% block content %}
<h1>Your Profile</h1>
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
<p><a href="{% url 'index' %}">Back to Home</a></p>
{% endblock %}
```

**Purpose:** Profile edit page for authenticated users.

### logout.html
```django
<h1>You have been logged out</h1>
<a href="{% url 'login' %}">Login again</a>
```

**Purpose:** Confirms logout; simple static page.

---

## 6 — Static Files

### styles.css (`blog/static/blog/css/styles.css`)
```css
/* Reset some default styles */


body { font-family: Arial; background-color: #f9f9f9; color: #333; }
header { background: #2c3e50; color: #fff; padding: 10px; }
ul { list-style: none; display: flex; }
ul li { margin-right: 20px; }
.content { max-width: 900px; margin: 20px auto; padding: 20px; background: #fff; }
button { padding: 10px 20px; background: #1abc9c; color: #fff; border: none; cursor: pointer; }
.message { color: green; }

```

**Purpose:** Styles pages, forms, buttons, and global messages.

### scripts.js (`blog/static/blog/js/scripts.js`)
```javascript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog page loaded');
});
```

**Purpose:** Placeholder JS for dynamic behavior. Can be extended for validation, alerts, etc.

---

## 7 — How It All Connects

1. User navigates to `/register/` → `register` view renders `register.html` using `RegisterForm`.

2. On submission, form is validated → user is created → `login()` logs them in → `messages.success` shows a message.

3. `base.html` displays messages and updates header nav depending on `user.is_authenticated`.

4. Login/logout/profile follow similar flow using built-in views and custom views.

5. Static files (CSS/JS) style the pages and add interactive behavior.