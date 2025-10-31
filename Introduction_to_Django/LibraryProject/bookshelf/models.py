from django.db import models

# Create your models here.
class Book(models.Model):
    # id's added automatically by Django
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField("year published")

    # defines an object represented as a string.
    # for own convenience & because objects’ representations
    # are used throughout Django’s automatically-generated admin
    def __str__(self):
        # special method that defines how an object is represented as a string.
        return f"'{self.title}', written by {self.author}, released in {self.publication_year}"