from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Profile(models.Model):
    """
    Extends Django's built-in User model with additional profile information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, help_text="Tell us about yourself")
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Email verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize image if too large
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
