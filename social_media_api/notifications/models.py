from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

User = settings.AUTH_USER_MODEL  # Use custom user model


class Notification(models.Model):
    # Who receives the notification
    recipient = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    # Who performed the action
    actor = models.ForeignKey(
        User,
        related_name='actions',
        on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)  # Action description: "liked your post"
    # Stores what kind of object the notification is about (Post, Comment, etc.)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    # Stores the ID of that object post with id = 5
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    # combines the two fields above to a real python object
    target = GenericForeignKey('target_content_type', 'target_object_id')
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} {self.verb} -> {self.recipient}"

'''
If user A likes user B’s post:

Field	                Value
recipient	            user B
actor	                user A
verb	                "liked your post"
target_content_type	     Post
target_object_id	     5
target	                 Post(id=5)
'''
