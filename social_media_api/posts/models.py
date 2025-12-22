from django.db import models
from django.conf import settings

# Create your models here.


User = settings.AUTH_USER_MODEL  # Use custom user model

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp when created
    updated_at = models.DateTimeField(auto_now=True)      # timestamp when updated

    def __str__(self):
        return f'{self.title} by {self.author}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


# Tracks which user liked which post
class Like(models.Model):
    user = models.ForeignKey(
        User,  # Reference to custom user
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'  # Allows post.likes.all()
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when liked

    class Meta:
        unique_together = ('user', 'post')  # Prevent multiple likes by same user

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
