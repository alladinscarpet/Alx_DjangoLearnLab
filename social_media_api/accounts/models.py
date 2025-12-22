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

    # Followers: users following THIS user
    # symmetrical=False → following is one-way
    # related_name='following' → allows user.following.all()
    # allows: “User A follows User B” without forcing B to follow A back.
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.username

