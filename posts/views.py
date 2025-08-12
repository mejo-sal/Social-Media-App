from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import IntegrityError
from .models import Post, Comment, Like
from .forms import PostCreateForm, CommentCreateForm
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
    
    # Add like information for each post
    for post in recent_posts:
        post.user_has_liked = Like.objects.filter(user=request.user, post=post).exists()
    
    # Get recent notifications
    notifications = user.notifications.filter(is_read=False)[:5]
    
    # Create a form instance for the modal
    post_form = PostCreateForm()
    
    context = {
        'user': user,
        'friends': friends,
        'friend_requests': friend_requests,
        'recent_posts': recent_posts,
        'notifications': notifications,
        'friends_count': len(friends),
        'friend_requests_count': friend_requests.count(),
        'notifications_count': notifications.count(),
        'post_form': post_form,  # Add form to context
    }
    
    return render(request, 'posts/home.html', context)


@login_required
def create_post(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('posts:home')
        else:
            messages.error(request, 'There was an error creating your post. Please try again.')
    
    # If GET request or form is invalid, redirect back to home
    return redirect('posts:home')


@login_required
def post_detail(request, pk):
    """Display a single post with all its comments"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user can view this post based on privacy settings
    if not can_view_post(request.user, post):
        messages.error(request, "You don't have permission to view this post.")
        return redirect('posts:home')
    
    # Get all comments for this post
    comments = post.comments.all().order_by('created_at')
    
    # Paginate comments (10 per page)
    paginator = Paginator(comments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Check if current user has liked this post
    user_has_liked = post.likes.filter(user=request.user).exists()
    
    # Handle comment form submission
    comment_form = CommentCreateForm()
    if request.method == 'POST':
        comment_form = CommentCreateForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('posts:post_detail', pk=post.pk)
    
    context = {
        'post': post,
        'comments': page_obj,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
        'is_own_post': post.author == request.user,
    }
    
    return render(request, 'posts/post_detail.html', context)


@login_required
def toggle_like(request, pk):
    """Toggle like/unlike for a post via AJAX"""
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        
        # Check if user can interact with this post
        if not can_view_post(request.user, post):
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        try:
            # Try to get existing like
            like = Like.objects.get(user=request.user, post=post)
            # If like exists, remove it (unlike)
            like.delete()
            liked = False
        except Like.DoesNotExist:
            # If like doesn't exist, create it
            Like.objects.create(user=request.user, post=post)
            liked = True
        
        # Return updated like count and status
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes_count,
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def can_view_post(user, post):
    """Check if a user can view a specific post based on privacy settings"""
    if post.privacy == 'public':
        return True
    elif post.privacy == 'private':
        return post.author == user
    elif post.privacy == 'friends':
        if post.author == user:
            return True
        # Check if they are friends using the correct field names
        return Friendship.objects.filter(
            from_user=post.author, 
            to_user=user, 
            status='accepted'
        ).exists() or Friendship.objects.filter(
            from_user=user, 
            to_user=post.author, 
            status='accepted'
        ).exists()
    return False
