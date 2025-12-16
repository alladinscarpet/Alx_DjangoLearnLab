# Comment Functionality Documentation

## Overview

The comment functionality adds interactivity to the blog by allowing users to engage with blog posts through comments.

- **Any authenticated user** can comment on any post
- **Only the comment author** can edit or delete their own comment
- **Comments are publicly visible** under each blog post
- **Post authors cannot delete comments** made by others (unless you later add moderation)

This design ensures fairness, ownership, and prevents abuse.

---

## Step 1: Defining the Comment Model

**File:** `blog/models.py`

### Purpose

The `Comment` model represents a single comment made by a user on a blog post.

### Code
```python
from django.db import models
from django.contrib.auth.models import User
from .models import Post

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
```

### Explanation

- **`post`**: Links each comment to a specific blog post
- **`author`**: The user who wrote the comment
- **`content`**: The comment text
- **`created_at`**: Timestamp when the comment was created
- **`updated_at`**: Timestamp when the comment was last edited
- **`related_name="comments"`** allows access via `post.comments.all()`

---

## Step 2: Creating the Comment Form

**File:** `blog/forms.py`

### Purpose

The `CommentForm` handles validation and input for creating and updating comments.

### Code
```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
```

### Explanation

- Uses Django's `ModelForm` to reduce boilerplate
- Only exposes the `content` field
- `author` and `post` are set automatically in the view (not user-controlled)
- Prevents users from impersonating others or attaching comments to the wrong post

---

## Step 3: Implementing Comment Views

**File:** `blog/views.py`

### Purpose

Views handle who can do what with comments and when.

### 1. Creating a Comment
```python
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Comment, Post
from .forms import CommentForm

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
```

**What this does:**
- Only logged-in users can comment
- Automatically assigns:
  - the logged-in user as the author
  - the correct post using `post_id` from the URL
- Redirects back to the post after submission

### 2. Updating a Comment
```python
from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
```

**What this does:**
- Only the comment author can edit
- Reuses the same form as comment creation
- Prevents unauthorized edits

### 3. Deleting a Comment
```python
from django.views.generic import DeleteView

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
```

**What this does:**
- Ensures only the author can delete their comment
- Shows a confirmation page before deletion
- Redirects back to the post after deletion

---

## Step 4: Templates for Comments

### 1. Displaying Comments (Inside Post Detail)

**File:** `blog/templates/blog/post_detail.html`
```django
<h3>Comments</h3>

<div class="comments-section">
  {% for comment in post.comments.all %}
    <div class="comment">
      <p>{{ comment.content }}</p>
      <small>
        By {{ comment.author }} · {{ comment.created_at|date:"M d, Y" }}
        {% if user == comment.author %}
          <a href="{% url 'comment-edit' comment.pk %}">Edit</a>
          <a href="{% url 'comment-delete' comment.pk %}">Delete</a>
        {% endif %}
      </small>
    </div>
  {% empty %}
    <p>No comments yet.</p>
  {% endfor %}
</div>

<a href="{% url 'comment-create' post.pk %}">Add Comment</a>
```

**Explanation:**
- Displays all comments related to a post
- Shows edit/delete links only to the comment author
- Uses the `related_name="comments"` from the model

### 2. Comment Form Template

**File:** `blog/templates/blog/comment_form.html`
```django
{% extends "blog/base.html" %}

{% block content %}
<h1>{{ view.object|yesno:"Edit Comment,Add Comment" }}</h1>

<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Save</button>
</form>

<a href="{% url 'post-list' %}">Cancel</a>
{% endblock %}
```

**Explanation:**
- Used for both creating and editing comments
- CSRF-protected
- Styled using existing CSS

### 3. Delete Confirmation Template

**File:** `blog/templates/blog/comment_confirm_delete.html`
```django
{% extends "blog/base.html" %}

{% block content %}
<h1>Delete Comment</h1>

<p>Are you sure you want to delete this comment?</p>

<form method="post">
  {% csrf_token %}
  <button type="submit">Yes, delete</button>
</form>

<a href="{% url 'post-detail' object.post.pk %}">Cancel</a>
{% endblock %}
```

---

## Step 5: URL Configuration

**File:** `blog/urls.py`
```python
from django.urls import path
from .views import (
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView
)

urlpatterns = [
    path(
        'posts/<int:post_id>/comments/new/',
        CommentCreateView.as_view(),
        name='comment-create'
    ),
    path(
        'comments/<int:pk>/edit/',
        CommentUpdateView.as_view(),
        name='comment-edit'
    ),
    path(
        'comments/<int:pk>/delete/',
        CommentDeleteView.as_view(),
        name='comment-delete'
    ),
]
```

**Explanation:**
- URLs are descriptive and REST-like
- Comment creation is nested under a post
- Edit/delete operate directly on the comment

---

## How Everything Connects (Big Picture)

### Post Detail Page
- Displays a blog post
- Fetches and shows related comments via `post.comments.all()`

### Comment Creation
1. User submits form
2. View assigns `post` + `author` automatically
3. Comment saved to database

### Comment Editing / Deleting
- Access controlled via `UserPassesTestMixin`
- Only the comment author can modify their comment

### Permissions
- Comments are public
- Ownership is enforced
- No user can modify another user's comment