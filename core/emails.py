from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from notifications.models import EmailLog


def send_friend_request_email(friendship):
    """Send email notification for friend request"""
    from_user = friendship.from_user
    to_user = friendship.to_user
    
    # Check if the recipient wants email notifications
    if not hasattr(to_user, 'settings'):
        return False
        
    user_settings = to_user.settings
    
    # Only send if both email notifications and friend request notifications are enabled
    if not (user_settings.email_notifications and user_settings.notify_friend_requests):
        return False
    
    try:
        subject = f'New Friend Request from {from_user.first_name} {from_user.last_name}'
        
        # Prepare context for email template
        context = {
            'from_user': from_user,
            'to_user': to_user,
            'site_name': 'SocialHub',
            'login_url': 'http://localhost:8002/accounts/login/',  # You can make this dynamic later
        }
        
        # Render email template
        message = render_to_string('core/emails/friend_request_email.html', context)
        
        # Send email
        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [to_user.email],
            html_message=message,
            fail_silently=False,
        )
        
        # Log successful email
        EmailLog.objects.create(
            recipient=to_user,
            email_type='friend_request',
            subject=subject,
            is_sent=True
        )
        
        return True
        
    except Exception as e:
        # Log failed email
        EmailLog.objects.create(
            recipient=to_user,
            email_type='friend_request',
            subject=f'New Friend Request from {from_user.first_name} {from_user.last_name}',
            is_sent=False,
            error_message=str(e)
        )
        return False


def send_friend_request_accepted_email(friendship):
    """Send email notification when friend request is accepted"""
    from_user = friendship.from_user  # Original sender
    to_user = friendship.to_user      # User who accepted
    
    # Check if the original sender wants email notifications
    if not hasattr(from_user, 'settings'):
        return False
        
    user_settings = from_user.settings
    
    # Only send if both email notifications and friend request notifications are enabled
    if not (user_settings.email_notifications and user_settings.notify_friend_requests):
        return False
    
    try:
        subject = f'{to_user.first_name} {to_user.last_name} accepted your friend request!'
        
        # Prepare context for email template
        context = {
            'from_user': from_user,
            'to_user': to_user,
            'site_name': 'SocialHub',
            'login_url': 'http://localhost:8002/accounts/login/',
        }
        
        # Render email template
        message = render_to_string('core/emails/friend_request_accepted_email.html', context)
        
        # Send email
        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [from_user.email],
            html_message=message,
            fail_silently=False,
        )
        
        # Log successful email
        EmailLog.objects.create(
            recipient=from_user,
            email_type='friend_request_accepted',
            subject=subject,
            is_sent=True
        )
        
        return True
        
    except Exception as e:
        # Log failed email
        EmailLog.objects.create(
            recipient=from_user,
            email_type='friend_request_accepted',
            subject=f'{to_user.first_name} {to_user.last_name} accepted your friend request!',
            is_sent=False,
            error_message=str(e)
        )
        return False
