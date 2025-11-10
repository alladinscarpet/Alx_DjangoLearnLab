from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# One Author can have Many Books (One-to-Many)
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Each Book has one Author (ForeignKey = Many-to-One)
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, max_length=100, on_delete=models.CASCADE, related_name='books')
    # Author = Target model
    # What Author will use to access Books
    # related_name creates a reverse relationship from Author to Book

    def __str__(self):
        return f"'{self.title}', written by {self.author}"


# Many Libraries can have Many Books (Many-to-Many)
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')
    # related_name lets you access Library related objects from the Books side.
    # instead of book.libray_set.all() we do book.libray.all()

    def __str__(self):
        return f"'{self.name}'"

# One Librarian manages One Library (One-to-One)
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return f"'{self.name}'"



# UserProfile Model (Extending Django’s User)
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'), # (value_in_db, human_readable_label)
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    # Django’s built-in User model does NOT have a role field.
    # So we create our own model connected 1–1 with User.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    # UserProfile.role has no influence on Django’s admin site, just 4 custom RBAC

    def __str__(self):
        return f"{self.user.username} - {self.role}"
