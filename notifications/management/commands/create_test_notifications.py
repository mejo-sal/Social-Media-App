from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notifications.models import Notification
import random


class Command(BaseCommand):
    help = 'Create test notifications for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username to create notifications for (default: admin)',
            default='admin'
        )
        parser.add_argument(
            '--count',
            type=int,
            help='Number of notifications to create (default: 10)',
            default=10
        )

    def handle(self, *args, **options):
        username = options['username']
        count = options['count']
        
        try:
            recipient = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist.')
            )
            return
        
        # Get some other users to be senders
        other_users = User.objects.exclude(id=recipient.id)[:5]
        
        if not other_users:
            self.stdout.write(
                self.style.ERROR('No other users found to create notifications from.')
            )
            return
        
        notification_types = [
            'friend_request',
            'friend_accept', 
            'like',
            'comment',
            'mention',
            'welcome'
        ]
        
        messages = {
            'friend_request': [
                'sent you a friend request.',
                'wants to connect with you.',
                'would like to be your friend.'
            ],
            'friend_accept': [
                'accepted your friend request!',
                'is now your friend!',
                'confirmed your friendship.'
            ],
            'like': [
                'liked your post.',
                'reacted to your photo.',
                'loved your update.'
            ],
            'comment': [
                'commented on your post.',
                'replied to your photo.',
                'left a comment on your update.'
            ],
            'mention': [
                'mentioned you in a post.',
                'tagged you in a comment.',
                'mentioned you in their update.'
            ],
            'welcome': [
                'Welcome to SocialHub!',
                'Thanks for joining our community!',
                'Your account has been created successfully.'
            ]
        }
        
        created_count = 0
        
        for i in range(count):
            # Random notification type
            notification_type = random.choice(notification_types)
            
            # Random sender (None for system notifications like welcome)
            if notification_type == 'welcome':
                sender = None
                message = random.choice(messages[notification_type])
            else:
                sender = random.choice(other_users)
                sender_name = sender.get_full_name() or sender.username
                message_template = random.choice(messages[notification_type])
                message = f'{sender_name} {message_template}'
            
            # Random read status (some read, some unread)
            is_read = random.choice([True, False, False])  # 33% read, 67% unread
            
            try:
                notification = Notification.create_notification(
                    recipient=recipient,
                    sender=sender,
                    notification_type=notification_type,
                    message=message
                )
                
                # Set random read status
                if is_read:
                    notification.mark_as_read()
                
                created_count += 1
                
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Failed to create notification: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} notifications for user "{username}".'
            )
        )
