from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserSettings


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    """Create UserSettings for new users"""
    if created:
        UserSettings.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_settings(sender, instance, **kwargs):
    """Ensure UserSettings exist when user is saved"""
    UserSettings.objects.get_or_create(user=instance)
