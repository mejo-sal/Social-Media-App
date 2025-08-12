from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Friendship


@login_required
def user_search_view(request):
    """Search for users by username"""
    query = request.GET.get('q', '').strip()
    users = []
    
    if query:
        # Search for users by username, first name, or last name
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)[:20]  # Limit to 20 results
        
        # Add friendship status for each user
        for user in users:
            user.friendship_status = get_friendship_status(request.user, user)
    
    return render(request, 'core/user_search.html', {
        'query': query,
        'users': users
    })


@login_required
def send_friend_request_view(request, user_id):
    """Send a friend request to a user"""
    if request.method == 'POST':
        to_user = get_object_or_404(User, id=user_id)
        friendship, message = Friendship.send_friend_request(request.user, to_user)
        
        if friendship:
            messages.success(request, message)
        else:
            messages.error(request, message)
    
    return redirect('user_search')


@login_required
def accept_friend_request_view(request, friendship_id):
    """Accept a friend request"""
    if request.method == 'POST':
        friendship = get_object_or_404(
            Friendship, 
            id=friendship_id, 
            to_user=request.user, 
            status='pending'
        )
        friendship.accept()
        messages.success(request, f'You are now friends with {friendship.from_user.username}!')
    
    return redirect('posts:home')


@login_required
def decline_friend_request_view(request, friendship_id):
    """Decline a friend request"""
    if request.method == 'POST':
        friendship = get_object_or_404(
            Friendship, 
            id=friendship_id, 
            to_user=request.user, 
            status='pending'
        )
        friendship.decline()
        messages.info(request, f'Friend request from {friendship.from_user.username} declined.')
    
    return redirect('posts:home')


def get_friendship_status(user1, user2):
    """Get the friendship status between two users"""
    if user1 == user2:
        return 'self'
    
    if Friendship.are_friends(user1, user2):
        return 'friends'
    
    # Check if user1 sent a request to user2
    sent_request = Friendship.objects.filter(
        from_user=user1, 
        to_user=user2, 
        status='pending'
    ).exists()
    
    if sent_request:
        return 'request_sent'
    
    # Check if user2 sent a request to user1
    received_request = Friendship.objects.filter(
        from_user=user2, 
        to_user=user1, 
        status='pending'
    ).exists()
    
    if received_request:
        return 'request_received'
    
    return 'none'
