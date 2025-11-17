from django.db import models

# custom user - Django only allows you to replace the user model ONCE, at the start of a project.
from django.contrib.auth.models import AbstractUser, BaseUserManager

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


# Custom User Manager - the factory that creates users and superusers
class CustomUserManager(BaseUserManager):
    # Defines how normal users are created
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    # Defines how admin users are created
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, email, password, **extra_fields)


# Custom User Class - the blueprint for user data
# Django’s default user, but I want to add more fields.
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    # The manager is attached to the model (Thus they MUST exist together)
    # replaces Django's default user creation logic with your new one.
    objects = CustomUserManager()

    def __str__(self):
        return self.username