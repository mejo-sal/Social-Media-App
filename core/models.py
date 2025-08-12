from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Friendship(models.Model):
    """
    Model for managing friendships between users
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('blocked', 'Blocked'),
    ]
    
    # The user who sent the friend request
    from_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_friend_requests'
    )
    
    # The user who received the friend request
    to_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_friend_requests'
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Ensure no duplicate friend requests
        unique_together = ('from_user', 'to_user')
        
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"
    
    @classmethod
    def are_friends(cls, user1, user2):
        """Check if two users are friends"""
        return cls.objects.filter(
            models.Q(from_user=user1, to_user=user2, status='accepted') |
            models.Q(from_user=user2, to_user=user1, status='accepted')
        ).exists()
    
    @classmethod
    def get_friends(cls, user):
        """Get all friends of a user"""
        friend_relationships = cls.objects.filter(
            models.Q(from_user=user, status='accepted') |
            models.Q(to_user=user, status='accepted')
        )
        
        friends = []
        for relationship in friend_relationships:
            if relationship.from_user == user:
                friends.append(relationship.to_user)
            else:
                friends.append(relationship.from_user)
        
        return friends
    
    @classmethod
    def send_friend_request(cls, from_user, to_user):
        """Send a friend request"""
        if from_user == to_user:
            return None, "You cannot send a friend request to yourself"
        
        if cls.are_friends(from_user, to_user):
            return None, "You are already friends"
        
        # Check if request already exists
        existing = cls.objects.filter(
            from_user=from_user, 
            to_user=to_user
        ).first()
        
        if existing:
            if existing.status == 'pending':
                return None, "Friend request already sent"
            elif existing.status == 'declined':
                existing.status = 'pending'
                existing.save()
                
                # Create notification for resent request
                from notifications.models import Notification
                Notification.create_notification(
                    recipient=to_user,
                    sender=from_user,
                    notification_type='friend_request',
                    message=f'{from_user.get_full_name() or from_user.username} sent you a friend request.',
                    content_object=existing
                )
                
                # Send email notification for resent request
                from .emails import send_friend_request_email
                send_friend_request_email(existing)
                
                return existing, "Friend request sent"
        
        # Create new friend request
        friendship = cls.objects.create(
            from_user=from_user,
            to_user=to_user,
            status='pending'
        )
        
        # Create notification
        from notifications.models import Notification
        Notification.create_notification(
            recipient=to_user,
            sender=from_user,
            notification_type='friend_request',
            message=f'{from_user.get_full_name() or from_user.username} sent you a friend request.',
            content_object=friendship
        )
        
        # Send email notification
        from .emails import send_friend_request_email
        send_friend_request_email(friendship)
        
        return friendship, "Friend request sent"
    
    def accept(self):
        """Accept the friend request"""
        self.status = 'accepted'
        self.save()
        
        # Create notification for the original sender
        from notifications.models import Notification
        Notification.create_notification(
            recipient=self.from_user,
            sender=self.to_user,
            notification_type='friend_accept',
            message=f'{self.to_user.get_full_name() or self.to_user.username} accepted your friend request!',
            content_object=self
        )
        
        # Send email notification to the original sender
        from .emails import send_friend_request_accepted_email
        send_friend_request_accepted_email(self)
    
    def decline(self):
        """Decline the friend request"""
        self.status = 'declined'
        self.save()
    
    def block(self):
        """Block the user"""
        self.status = 'blocked'
        self.save()
