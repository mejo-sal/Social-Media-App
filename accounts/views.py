from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.core.paginator import Paginator
import uuid

from .models import Profile
from .forms import UserRegistrationForm, UserLoginForm, PasswordResetRequestForm, ProfileUpdateForm
from notifications.models import Notification, EmailLog
from posts.models import Post, Like


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user but don't activate yet
            user = form.save(commit=False)
            user.is_active = False  # User must verify email first
            user.save()
            
            # Create profile (should be auto-created by signal, but let's ensure)
            profile, created = Profile.objects.get_or_create(user=user)
            
            # Generate email verification token
            verification_token = str(uuid.uuid4())
            profile.email_verification_token = verification_token
            profile.save()
            
            # Send verification email instead of welcome email
            send_verification_email(user, request)
            
            messages.success(
                request, 
                f'Registration successful! Please check your email ({user.email}) to verify your account before logging in.'
            )
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Check if user exists first
            try:
                user_obj = User.objects.get(username=username)
                if not user_obj.is_active:
                    messages.error(request, 'Please verify your email address before logging in. Check your inbox for the verification link.')
                    return render(request, 'accounts/login.html', {'form': form})
            except User.DoesNotExist:
                pass  # Will be handled by authenticate below
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                
                # Redirect to next page if provided, otherwise home
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def verify_email(request, token):
    """Verify user email with token"""
    try:
        profile = Profile.objects.get(email_verification_token=token)
        user = profile.user
        
        if not user.is_active:
            # Activate the user
            user.is_active = True
            user.save()
            
            # Clear the verification token
            profile.email_verification_token = ''
            profile.save()
            
            # Send welcome email now
            send_welcome_email(user)
            
            # Create welcome notification
            Notification.create_notification(
                recipient=user,
                sender=None,
                notification_type='welcome',
                message=f"Welcome to SocialHub, {user.first_name or user.username}!"
            )
            
            messages.success(request, 'Email verified successfully! You can now log in to your account.')
            return redirect('login')
        else:
            messages.info(request, 'Email is already verified. You can log in to your account.')
            return redirect('login')
            
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid verification link. Please try registering again.')
        return redirect('register')


def resend_verification_email(request):
    """Resend verification email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_active=False)
            if user.profile.email_verification_token:
                send_verification_email(user, request)
                messages.success(request, f'Verification email resent to {email}. Please check your inbox.')
            else:
                messages.info(request, 'Your email is already verified. You can log in.')
        except User.DoesNotExist:
            messages.error(request, 'No unverified account found with this email address.')
        
        return redirect('login')
    
    return render(request, 'accounts/resend_verification.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


def password_reset_request_view(request):
    """Password reset request view"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                
                # Generate password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Send password reset email
                send_password_reset_email(user, uid, token, request)
                
                messages.success(request, 'Password reset instructions have been sent to your email.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email address.')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'accounts/password_reset_request.html', {'form': form})


def password_reset_confirm_view(request, uidb64, token):
    """Password reset confirmation view"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                password = request.POST.get('password')
                password_confirm = request.POST.get('password_confirm')
                
                if password and password == password_confirm:
                    if len(password) >= 8:
                        user.set_password(password)
                        user.save()
                        messages.success(request, 'Your password has been reset successfully. You can now log in.')
                        return redirect('login')
                    else:
                        messages.error(request, 'Password must be at least 8 characters long.')
                else:
                    messages.error(request, 'Passwords do not match.')
            
            return render(request, 'accounts/password_reset_confirm.html', {
                'validlink': True,
                'uidb64': uidb64,
                'token': token
            })
        else:
            messages.error(request, 'This password reset link is invalid or has expired.')
            return redirect('password_reset_request')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'This password reset link is invalid.')
        return redirect('password_reset_request')


@login_required
def profile_view(request, username=None):
    """User profile view"""
    if username:
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        is_own_profile = request.user == user
    else:
        user = request.user
        profile = request.user.profile
        is_own_profile = True
    
    # Get user's posts
    if is_own_profile:
        # Show all posts if it's the user's own profile
        posts = Post.objects.filter(author=user).order_by('-created_at')
    else:
        # Show only public posts for other users (we'll add friend logic later)
        posts = Post.objects.filter(author=user, privacy='public').order_by('-created_at')
    
    # Paginate posts
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Add like information for each post if user is authenticated
    if request.user.is_authenticated:
        for post in page_obj:
            post.user_has_liked = Like.objects.filter(user=request.user, post=post).exists()
    
    context = {
        'profile_user': user,
        'profile': profile,
        'is_own_profile': is_own_profile,
        'posts': page_obj,
        'posts_count': posts.count(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    """Edit user profile view"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})


def send_welcome_email(user):
    """Send welcome email to new user"""
    try:
        subject = 'Welcome to SocialHub!'
        message = render_to_string('accounts/emails/welcome_email.html', {
            'user': user,
            'site_name': 'SocialHub'
        })
        
        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,
            fail_silently=False,
        )
        
        # Log email
        EmailLog.objects.create(
            recipient=user,
            email_type='welcome',
            subject=subject,
            is_sent=True
        )
    except Exception as e:
        # Log failed email
        EmailLog.objects.create(
            recipient=user,
            email_type='welcome',
            subject='Welcome to SocialHub!',
            is_sent=False,
            error_message=str(e)
        )


def send_verification_email(user, request):
    """Send email verification email to new user"""
    try:
        # Create verification URL
        verification_url = request.build_absolute_uri(
            reverse('verify_email', kwargs={'token': user.profile.email_verification_token})
        )
        
        subject = 'Verify Your SocialHub Email Address'
        message = render_to_string('accounts/emails/verification_email.html', {
            'user': user,
            'verification_url': verification_url,
            'site_name': 'SocialHub'
        })
        
        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,
            fail_silently=False,
        )
        
        # Log email
        EmailLog.objects.create(
            recipient=user,
            email_type='email_verification',
            subject=subject,
            is_sent=True
        )
    except Exception as e:
        # Log failed email
        EmailLog.objects.create(
            recipient=user,
            email_type='email_verification',
            subject='Verify Your SocialHub Email Address',
            is_sent=False,
            error_message=str(e)
        )


def send_password_reset_email(user, uid, token, request):
    """Send password reset email"""
    try:
        reset_url = request.build_absolute_uri(
            reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        )
        
        subject = 'Reset Your SocialHub Password'
        message = render_to_string('accounts/emails/password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
            'site_name': 'SocialHub'
        })
        
        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,
            fail_silently=False,
        )
        
        # Log email
        EmailLog.objects.create(
            recipient=user,
            email_type='password_reset',
            subject=subject,
            is_sent=True
        )
    except Exception as e:
        # Log failed email
        EmailLog.objects.create(
            recipient=user,
            email_type='password_reset',
            subject='Reset Your SocialHub Password',
            is_sent=False,
            error_message=str(e)
        )
