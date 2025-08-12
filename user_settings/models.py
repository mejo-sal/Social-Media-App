from django.db import models
from django.contrib.auth.models import User


class UserSettings(models.Model):
    """
    Model for user privacy and notification settings
    """
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends Only'),
        ('private', 'Private'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    
    # Privacy Settings
    profile_visibility = models.CharField(
        max_length=10, 
        choices=PRIVACY_CHOICES, 
        default='public',
        help_text="Who can see your profile"
    )
    default_post_privacy = models.CharField(
        max_length=10, 
        choices=PRIVACY_CHOICES, 
        default='public',
        help_text="Default privacy for new posts"
    )
    allow_friend_requests = models.BooleanField(
        default=True,
        help_text="Allow others to send you friend requests"
    )
    show_email = models.BooleanField(
        default=False,
        help_text="Show email on your profile"
    )
    show_birth_date = models.BooleanField(
        default=True,
        help_text="Show birth date on your profile"
    )
    
    # Notification Settings
    email_notifications = models.BooleanField(
        default=True,
        help_text="Receive email notifications"
    )
    notify_friend_requests = models.BooleanField(
        default=True,
        help_text="Get notified of new friend requests"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Settings"
    
    class Meta:
        verbose_name = "User Settings"
        verbose_name_plural = "User Settings"
