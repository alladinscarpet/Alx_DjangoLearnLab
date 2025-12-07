# API Enhancements: Filtering, Searching & Ordering

**File:** `api/views.py`, `api/filters.py`, `settings.py`

This section documents how filtering, searching, and ordering were added to the Book API.

---

## 1️⃣ Filtering Setup

### Install dependency
```bash
pip install django-filter
```

### Enable globally

**`settings.py`**
```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

Enables DRF's built-in filtering, search, and ordering engines.

### Create a FilterSet

**`api/filters.py`**
```python
import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
            'author__name': ['icontains'], 
        }
```

Defines which model fields can be filtered and which lookup types are allowed.

---

## 2️⃣ Add Filtering, Search & Ordering to the View

**`api/views.py`**
```python
from rest_framework import generics, renderers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Enable filtering, search & ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

    # Allow both JSON & Browsable API
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]
```

### What each does

- **`filter_backends`**: Activates filtering engines.
- **`filterset_class`**: Applies our `BookFilter` rules.
- **`search_fields`**: Enables keyword search.
- **`ordering_fields`**: Allows sorting results.
- **`renderer_classes`**: Keeps the Browsable API while still returning JSON to tools like Postman.

**Note:** Ensure `django_filters` is added to `INSTALLED_APPS` so DRF can load filter templates in browsable API UI

---

## 3️⃣ Sample API Queries

### 🔎 Filtering

| Field | Lookup | Sample URL                                    | Meaning |
|-------|--------|-----------------------------------------------|---------|
| `title` | `exact` | `/api/books/?title=Moses`                     | Title matches exactly |
| `title` | `icontains` | `/api/books/?title__icontains=python`         | Title contains text |
| `publication_year` | `exact` | `/api/books/?publication_year=2023`           | Matches year |
| `publication_year` | `gte` | `/api/books/?publication_year__gte=2020`      | Year ≥ 2020 |
| `publication_year` | `lte` | `/api/books/?publication_year__lte=2022`      | Year ≤ 2022 |
| `author__name` | `icontains` | `/api/books/?author__name__icontains=rowling` | Filter by author name |

### 🔍 Searching
```
/api/books/?search=magic
/api/books/?search=rowling
```

### ↕ Ordering
```
/api/books/?ordering=title
/api/books/?ordering=-publication_year
```

### Combine them
```
/api/books/?search=python&publication_year__gte=2015&ordering=-title
```

---

##  Summary

By enabling DRF filter backends, creating a `FilterSet`, and configuring `BookListView`, the API now supports:

- Precise field filtering
- Text search across fields
- Custom ordering
- Full Browsable API + JSON output

This improves data accessibility and usability for both developers and frontend clients.