from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# One Author can have Many Books (One-to-Many)
class Book(models.Model):
    title = models.CharField(max_length=120)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, max_length=100, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"'{self.title}', written by {self.author} in {self.publication_year}"

