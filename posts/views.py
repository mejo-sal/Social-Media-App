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
    
    # Get recent posts (we'll add posts functionality later)
    recent_posts = Post.objects.filter(privacy='public').order_by('-created_at')[:10]
    
    # Get recent notifications
    notifications = user.notifications.filter(is_read=False)[:5]
    
    # Get friend suggestions (users who are not friends yet)
    existing_friend_ids = [friend.id for friend in friends] + [user.id]
    suggested_friends = User.objects.exclude(id__in=existing_friend_ids)[:5]
    
    context = {
        'user': user,
        'friends': friends,
        'recent_posts': recent_posts,
        'notifications': notifications,
        'suggested_friends': suggested_friends,
        'friends_count': len(friends),
        'notifications_count': notifications.count(),
    }
    
    return render(request, 'posts/home.html', context)


@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'accounts/profile.html', {'user': request.user})
