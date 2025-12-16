from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.



class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    published_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # django-taggit handles tag tables internally
    tags = TaggableManager(blank=True)  # <-- django-taggit that stores unique tags for posts

    def __str__(self):
        return f'{self.title} by {self.author}'

    # This makes Django automatically redirect to /posts/<pk>/ after creation or update.
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

# many comments → one post
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"



