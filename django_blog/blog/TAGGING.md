# Tagging and Search Functionality Documentation

## Objective

Enable posts to be categorized using tags and allow users to filter posts by these tags. Additionally, implement search functionality so users can find posts by keywords in titles, content, or tags. These features improve content organization and make it easier for users to discover relevant posts.

---

## Step 1: Tag Model

**Location:** `blog/models.py`

```python
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    published_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')  # <-- Tags

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
```

### Explanation:

- `ManyToManyField` allows each post to have multiple tags and each tag to belong to multiple posts.
- `blank=True` allows posts to exist without tags.
- `get_absolute_url()` helps redirect after post creation or update.

---

## Step 2: Update Post Form

**Location:** `blog/forms.py`

```python
from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Include tags
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
            'content': forms.Textarea(attrs={'rows': 10}),
        }
```

### Explanation:

- `ModelMultipleChoiceField` allows selecting multiple tags.
- `CheckboxSelectMultiple` displays tags as checkboxes.
- Users can assign tags when creating or updating a post.

---

## Step 3: Display Tags in Post Detail Template

**Location:** `blog/templates/blog/post_detail.html`

```html
<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>

<!-- Display associated tags -->
<p>Tags:
    {% for tag in post.tags.all %}
        <a href="{% url 'tagged-posts' tag.name %}">{{ tag.name }}</a>{% if not forloop.last %}, {% endif %}
    {% empty %}
        No tags
    {% endfor %}
</p>

<hr>

<h2>Comments</h2>
...
```

### Explanation:

- Loops through all tags assigned to the post.
- Each tag links to a filtered list page handled by `TaggedPostListView`.

---

## Step 4: Tagged Post List View

**Location:** `blog/views.py`

```python
from django.views.generic import ListView
from .models import Post, Tag

class TaggedPostListView(ListView):
    model = Post
    template_name = 'blog/tagged_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name__iexact=tag_name).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs.get('tag_name')
        return context
```

### Explanation:

- Filters posts to show only those with the selected tag.
- `tags__name__iexact` ensures case-insensitive matching.
- `get_context_data()` passes the tag name to the template.

---

## Step 5: Tagged Posts Template

**Location:** `blog/templates/blog/tagged_posts.html`

```html
{% extends "blog/base.html" %}
{% block title %}Posts tagged "{{ tag_name }}"{% endblock %}

{% block content %}
<h1>Posts tagged "{{ tag_name }}"</h1>

{% for post in posts %}
    <div>
        <h2><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h2>
        <p>{{ post.content|truncatewords:30 }}</p>
    </div>
{% empty %}
    <p>No posts found for this tag.</p>
{% endfor %}
{% endblock %}
```

### Explanation:

- Displays posts filtered by the selected tag.
- Shows title and truncated content for a preview.
- Handles the case where no posts exist for a tag.

---

## Step 6: Search Functionality

**Location:** `blog/views.py`

```python
from django.db.models import Q
from django.shortcuts import render
from .models import Post

def search(request):
    """
    Handles search requests by filtering posts by title, content, or tags.
    """
    query = request.GET.get('q', '')  # Get query from URL parameter
    posts = Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})
```

### Explanation:

- Uses `Q` objects for OR queries: matches title, content, or tag names.
- `.distinct()` ensures no duplicate posts.
- Sends filtered posts to `search_results.html` along with the search query.

---

## Step 7: Search Results Template

**Location:** `blog/templates/blog/search_results.html`

```html
{% extends "blog/base.html" %}
{% block title %}Search results{% endblock %}

{% block content %}
<h1>Search results for "{{ query }}"</h1>

{% for post in posts %}
    <div>
        <h2><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h2>
        <p>{{ post.content|truncatewords:30 }}</p>
    </div>
{% empty %}
    <p>No posts match your search.</p>
{% endfor %}
{% endblock %}
```

### Explanation:

- Displays posts matching the search query.
- Shows post title and preview content.
- Handles the case where no posts match the query.

---

## Step 8: URL Configuration

**Location:** `blog/urls.py`

```python
# Search
path('search/', views.search, name='search'),

# View posts by tag
path('tags/<str:tag_name>/', views.TaggedPostListView.as_view(), name='tagged-posts'),
```

### Explanation:

- `/search/` maps to the search view: receives GET requests from the search bar.
- `/tags/<tag_name>/` maps to `TaggedPostListView` to filter posts by tag.

---

## Step 9: How Everything Works Together

### Post Creation/Editing:
- Users assign tags via the `PostForm`.
- Tags are stored in the database with a many-to-many relationship.

### Post Display:
- `post_detail.html` shows clickable tags for each post.
- Tags link to `/tags/<tag_name>/` pages.

### Filtering by Tag:
- `TaggedPostListView` filters posts by selected tag.
- Template displays a list of matching posts.

### Search Functionality:
- Users type a query in the search bar.
- URL `/search/?q=<query>` triggers `search()` view.
- `search_results.html` displays posts matching title, content, or tags.

### Integration:
- Tagging and search improve post discovery.
- Works seamlessly with post CRUD and templates.

---

## Summary

**Tagging** allows posts to be categorized and filtered.

**Search** lets users find posts by title, content, or tag keywords.

### Users can:
- Assign tags when creating/editing posts.
- Click on tags to filter posts.
- Search across posts and tags.

These features connect models, forms, templates, views, and URLs, enhancing content organization and user experience.