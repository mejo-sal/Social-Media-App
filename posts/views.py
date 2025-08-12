from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post
from accounts.models import Profile
from core.models import Friendship
from notifications.models import Notification


@login_required
def home_view(request):
    """Homepage view for logged-in users"""
    user = request.user
    
    # Get user's friends
    friends = Friendship.get_friends(user)
    
    # Get pending friend requests (received)
    friend_requests = Friendship.objects.filter(
        to_user=user,
        status='pending'
    ).order_by('-created_at')
    
    # Get recent posts (we'll add posts functionality later)
    recent_posts = Post.objects.filter(privacy='public').order_by('-created_at')[:10]
    
    # Get recent notifications
    notifications = user.notifications.filter(is_read=False)[:5]
    
    context = {
        'user': user,
        'friends': friends,
        'friend_requests': friend_requests,
        'recent_posts': recent_posts,
        'notifications': notifications,
        'friends_count': len(friends),
        'friend_requests_count': friend_requests.count(),
        'notifications_count': notifications.count(),
    }
    
    return render(request, 'posts/home.html', context)
