from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone


class Notification(models.Model):
    """
    Model for user notifications
    """
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('friend_request', 'Friend Request'),
        ('friend_accept', 'Friend Request Accepted'),
        ('mention', 'Mention'),
        ('welcome', 'Welcome'),
    ]
    
    # Who receives the notification
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    
    # Who triggered the notification (can be null for system notifications)
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_notifications',
        null=True,
        blank=True
    )
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.CharField(max_length=255)
    
    # Generic foreign key to link to any model (Post, Comment, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Notification status
    is_read = models.BooleanField(default=False)
    is_sent_via_email = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Notification to {self.recipient.username}: {self.message}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    @classmethod
    def create_notification(cls, recipient, sender, notification_type, message, content_object=None):
        """Helper method to create notifications"""
        notification = cls.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            message=message,
            content_object=content_object
        )
        return notification


class EmailLog(models.Model):
    """
    Model to track sent emails
    """
    EMAIL_TYPES = [
        ('welcome', 'Welcome Email'),
        ('password_reset', 'Password Reset'),
        ('email_verification', 'Email Verification'),
        ('notification', 'Notification Email'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_logs')
    email_type = models.CharField(max_length=20, choices=EMAIL_TYPES)
    subject = models.CharField(max_length=255)
    
    # Email status
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        status = "Sent" if self.is_sent else "Failed"
        return f"{self.email_type} to {self.recipient.username} - {status}"
