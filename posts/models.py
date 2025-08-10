from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    """
    Model for user posts containing text and/or images
    """
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends Only'),
        ('private', 'Private'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=2000, help_text="What's on your mind?")
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # For tracking engagement
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']  # Show newest posts first
        
    def __str__(self):
        return f"{self.author.username} - {self.content[:50]}..."
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def update_likes_count(self):
        """Update the likes count for this post"""
        self.likes_count = self.likes.count()
        self.save(update_fields=['likes_count'])
    
    def update_comments_count(self):
        """Update the comments count for this post"""
        self.comments_count = self.comments.count()
        self.save(update_fields=['comments_count'])


class Comment(models.Model):
    """
    Model for comments on posts
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']  # Show oldest comments first
        
    def __str__(self):
        return f"{self.author.username} on {self.post.author.username}'s post"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the post's comment count
        self.post.update_comments_count()
    
    def delete(self, *args, **kwargs):
        post = self.post
        super().delete(*args, **kwargs)
        # Update the post's comment count after deletion
        post.update_comments_count()


class Like(models.Model):
    """
    Model for tracking user likes on posts
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        # Ensure a user can only like a post once
        unique_together = ('user', 'post')
        
    def __str__(self):
        return f"{self.user.username} likes {self.post.author.username}'s post"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the post's like count
        self.post.update_likes_count()
    
    def delete(self, *args, **kwargs):
        post = self.post
        super().delete(*args, **kwargs)
        # Update the post's like count after deletion
        post.update_likes_count()
