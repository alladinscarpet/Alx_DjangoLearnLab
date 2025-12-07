# Model and Serializer Setup (Summary)

## Models Overview

The project defines two core models to represent authors and their books:

### Author
- Stores an author's name.
- Has a one-to-many relationship with books (one author can write many books).
- Relationship is enabled through the `related_name='books'` on the Book model.

### Book
- Stores a book's title and year of publication.
- Linked to an author through a `ForeignKey`, enforcing referential integrity and cascading deletes.

This structure allows easy querying of all books written by a specific author.

---

## Serializers Overview

### BookSerializer
- Serializes all fields of the Book model.
- Implements custom validation to ensure the `publication_year` is not in the future.
- Acts as the base serializer for nested book data within authors.

### AuthorSerializer
- Serializes the author's `id` and `name`.
- Includes a nested list of serialized books via:
```python
  books = BookSerializer(many=True, read_only=True)
```

- Uses the `related_name='books'` defined in the Book model, automatically pulling all books associated with that author.

---

## How the Author–Book Relationship Is Handled in Serialization

The relationship is managed through Django's reverse relation and DRF's nested serializers:

- Each **Book** has a foreign key pointing to an **Author**.
- DRF uses the reverse relation (`author.books`) to gather all books linked to an author.
- The `AuthorSerializer` includes a `books` field that nests `BookSerializer` for every related book.
- This produces an output where each author object contains an embedded list of their books:
```json
{
  "id": 1,
  "name": "Chinua Achebe",
  "books": [
    {
      "id": 5,
      "title": "Things Fall Apart",
      "publication_year": 1958,
      "author": 1
    }
  ]
}
```

---

## Implement & Test

You can quickly test your models and serializers in the Django shell:
```bash
python manage.py shell
```
```python
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

# Create an author
a = Author.objects.create(name="J.K. Rowling")

# Create a book for that author
b = Book.objects.create(title="HP 1", publication_year=1997, author=a)

# Serialize author with nested books
AuthorSerializer(a).data
```

**Expected output:**
```python
{
  "id": 1,
  "name": "J.K. Rowling",
  "books": [
    {
      "id": 1,
      "title": "HP 1",
      "publication_year": 1997,
      "author": 1
    }
  ]
}
```