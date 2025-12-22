from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# Custom User Class - the blueprint for user data
# Django’s default user, but I want to add more fields.
class User(AbstractUser):
    # Short bio shown on profile
    bio = models.TextField(blank=True)

    # profile picture
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    # Single ManyToMany field to represent who this user is following
    following = models.ManyToManyField(
        'self',  # Self-referential
        symmetrical=False,  # One-way relationship
        related_name='followers',  # Reverse lookup to get all followers of a user
        blank=True
    )



    def __str__(self):
        return self.username

'''
# tell Django to point to new custom user model in settings.py
AUTH_USER_MODEL = 'accounts.User'
'''

