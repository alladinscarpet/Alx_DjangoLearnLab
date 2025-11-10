'''Automate reactions (e.g., create profile when user is created).'''
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    When a new User is created, automatically create a UserProfile.
    Default role = Member.
    """
    if created:
        UserProfile.objects.create(user=instance, role='Member')


@receiver(post_save, sender=UserProfile)
def update_user_role_permissions(sender, instance, **kwargs):
    """
    When UserProfile is saved, update User.is_staff based on role:
    - Admin role → is_staff = True
    - Any other role → is_staff = False
    """
    user = instance.user

    if instance.role == 'Admin':
        user.is_staff = True
    else:
        user.is_staff = False

    user.save()

