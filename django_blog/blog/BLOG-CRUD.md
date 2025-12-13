# Blog Post Management (CRUD) — Documentation & Implementation

This section documents how blog post creation, viewing, editing, and deletion are implemented in your Django blog project.

We focus only on CRUD, not authentication (already documented earlier).

---

## 1. Model (Data Layer)

### blog/models.py
```python
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    published_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
```

### What this does & why it's required

| Part | Purpose |
|------|---------|
| `title`, `content` | Core blog post data |
| `author` | Links each post to a user (ownership + permissions) |
| `published_date` | When the post was created |
| `updated_at` | Tracks edits |
| `__str__` | Makes admin/debugging readable |
| `get_absolute_url()` | Tells Django where to redirect after create/update |

💡 **Why `get_absolute_url` matters**  
Class-based views (`CreateView`, `UpdateView`) automatically redirect to this URL if no `success_url` is provided.

---

## 2. Forms (Input Layer)

### blog/forms.py (CRUD-relevant part only)
```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """
    ModelForm for creating and editing blog posts.
    Author is excluded because it is set automatically in the view.
    """
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Post title'
            }),
            'content': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': 'Write your post here...'
            }),
        }
```

### Why this exists

- Converts HTML form input → validated `Post` object
- Prevents users from choosing their own author
- Ensures safe, validated data reaches the database
- Reused by `CreateView` and `UpdateView`

---

## 3. Views (Business Logic)

### CRUD Class-Based Views — blog/views.py
```python
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm
```

### 3.1 List All Posts
```python
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
```

**What it does:**
- Fetches all posts
- Passes them to the template as `posts`
- Automatically handles pagination

**Who can access:** Everyone (no authentication required)

### 3.2 View a Single Post
```python
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
```

**What it does:**
- Fetches one `Post` by primary key
- Exposes it as `post` in the template

### 3.3 Create a Post
```python
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

**Why this matters:**
- `LoginRequiredMixin` → only logged-in users can create posts
- Automatically handles:
  - GET → show form
  - POST → validate & save
- `author` is set securely server-side

### 3.4 Update a Post
```python
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
```

**Security logic:**
- Must be logged in
- Must be the author
- Otherwise → 403 Forbidden

### 3.5 Delete a Post
```python
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
```

**Why `DeleteView`:**
- Forces explicit confirmation
- Prevents accidental deletion
- Enforces ownership

---

## 4. URLs (Routing Layer)

### blog/urls.py (CRUD section)
```python
urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/create/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]
```

**Why this structure:**
- REST-like
- Predictable
- Easy to reason about
- Matches Django CBV expectations

---

## 5. Templates (Presentation Layer)

All templates live in: **`blog/templates/blog/`**

### 5.1 Post List — post_list.html
```django
{% extends "blog/base.html" %}

{% block content %}
<h1>All Blog Posts</h1>

{% if user.is_authenticated %}
  <a href="{% url 'post-create' %}">Create New Post</a>
{% endif %}

<ul>
  {% for post in posts %}
    <li>
      <a href="{% url 'post-detail' post.pk %}">
        {{ post.title }}
      </a>
      <small>by {{ post.author }}</small>
    </li>
  {% empty %}
    <p>No posts yet.</p>
  {% endfor %}
</ul>
{% endblock %}
```

### 5.2 Post Detail — post_detail.html
```django
{% extends "blog/base.html" %}

{% block content %}
<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>
<p><small>By {{ post.author }} on {{ post.published_date }}</small></p>

{% if user == post.author %}
  <a href="{% url 'post-update' post.pk %}">Edit</a>
  <a href="{% url 'post-delete' post.pk %}">Delete</a>
{% endif %}

<a href="{% url 'post-list' %}">Back to posts</a>
{% endblock %}
```

### 5.3 Create / Edit Form — post_form.html
```django
{% extends "blog/base.html" %}

{% block content %}
<h1>{{ view.object|yesno:"Edit Post,Create Post" }}</h1>

<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Save</button>
</form>

<a href="{% url 'post-list' %}">Cancel</a>
{% endblock %}
```

### 5.4 Delete Confirmation — post_confirm_delete.html
```django
{% extends "blog/base.html" %}

{% block content %}
<h1>Delete Post</h1>

<p>Are you sure you want to delete "{{ object.title }}"?</p>

<form method="post">
  {% csrf_token %}
  <button type="submit">Yes, delete</button>
</form>

<a href="{% url 'post-detail' object.pk %}">Cancel</a>
{% endblock %}
```

---

## 6. Permissions & Access Control (Recap)

| View | Access |
|------|--------|
| List | Everyone |
| Detail | Everyone |
| Create | Logged-in users |
| Update | Logged-in + author only |
| Delete | Logged-in + author only |

**Implemented using:**
- `LoginRequiredMixin`
- `UserPassesTestMixin`
- `test_func()` comparing `post.author`

---

## 7. How It All Connects (Mental Model)

Think of your CRUD system as layers:
```
User
 ↓
URL (routes request)
 ↓
View (logic + permissions)
 ↓
Form (validation)
 ↓
Model (database)
 ↓
Template (HTML response)
```

### Example: Creating a Post

1. User visits `/posts/create/`
2. `PostCreateView` checks authentication
3. `PostForm` validates input
4. `author` is injected automatically
5. Post saved to DB
6. Redirect to post list