from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from user_settings.models import UserSettings
from django.db import transaction
import random


class Command(BaseCommand):
    help = 'Seed the database with test users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Sample user data
        sample_users = [
            {
                'username': 'alice_johnson',
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'email': 'alice.johnson@example.com',
                'bio': 'Software developer passionate about Python and Django. Love hiking and photography.',
                'location': 'San Francisco, CA'
            },
            {
                'username': 'bob_smith',
                'first_name': 'Bob',
                'last_name': 'Smith',
                'email': 'bob.smith@example.com',
                'bio': 'Graphic designer and coffee enthusiast. Always looking for creative inspiration.',
                'location': 'New York, NY'
            },
            {
                'username': 'carol_davis',
                'first_name': 'Carol',
                'last_name': 'Davis',
                'email': 'carol.davis@example.com',
                'bio': 'Teacher and book lover. Passionate about education and learning new things.',
                'location': 'Chicago, IL'
            },
            {
                'username': 'david_wilson',
                'first_name': 'David',
                'last_name': 'Wilson',
                'email': 'david.wilson@example.com',
                'bio': 'Marketing professional and fitness enthusiast. Love running and healthy living.',
                'location': 'Los Angeles, CA'
            },
            {
                'username': 'emma_brown',
                'first_name': 'Emma',
                'last_name': 'Brown',
                'email': 'emma.brown@example.com',
                'bio': 'Data scientist working with machine learning. Enjoy traveling and trying new cuisines.',
                'location': 'Seattle, WA'
            },
            {
                'username': 'frank_taylor',
                'first_name': 'Frank',
                'last_name': 'Taylor',
                'email': 'frank.taylor@example.com',
                'bio': 'Musician and songwriter. Playing guitar for 15 years and love jazz music.',
                'location': 'Nashville, TN'
            },
            {
                'username': 'grace_martinez',
                'first_name': 'Grace',
                'last_name': 'Martinez',
                'email': 'grace.martinez@example.com',
                'bio': 'Photographer and visual artist. Capturing beautiful moments and sharing stories.',
                'location': 'Austin, TX'
            },
            {
                'username': 'henry_garcia',
                'first_name': 'Henry',
                'last_name': 'Garcia',
                'email': 'henry.garcia@example.com',
                'bio': 'Chef and food blogger. Exploring flavors from around the world.',
                'location': 'Miami, FL'
            },
            {
                'username': 'isabel_rodriguez',
                'first_name': 'Isabel',
                'last_name': 'Rodriguez',
                'email': 'isabel.rodriguez@example.com',
                'bio': 'Environmental scientist and nature lover. Working towards a sustainable future.',
                'location': 'Portland, OR'
            },
            {
                'username': 'jack_lee',
                'first_name': 'Jack',
                'last_name': 'Lee',
                'email': 'jack.lee@example.com',
                'bio': 'Game developer and tech enthusiast. Building the next generation of interactive experiences.',
                'location': 'San Jose, CA'
            },
            {
                'username': 'karen_white',
                'first_name': 'Karen',
                'last_name': 'White',
                'email': 'karen.white@example.com',
                'bio': 'Nurse and healthcare advocate. Dedicated to helping others and making a difference.',
                'location': 'Boston, MA'
            },
            {
                'username': 'luke_anderson',
                'first_name': 'Luke',
                'last_name': 'Anderson',
                'email': 'luke.anderson@example.com',
                'bio': 'Financial analyst and investment enthusiast. Always learning about markets and economics.',
                'location': 'Denver, CO'
            }
        ]

        # Use only the number of users requested
        users_to_create = sample_users[:count]
        
        created_users = []
        
        with transaction.atomic():
            for user_data in users_to_create:
                # Check if user already exists
                if User.objects.filter(username=user_data['username']).exists():
                    self.stdout.write(
                        self.style.WARNING(f'User {user_data["username"]} already exists, skipping...')
                    )
                    continue
                
                # Create user
                user = User.objects.create_user(
                    username=user_data['username'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    password='testpass123'  # Same password for all test users
                )
                
                # Update profile (should be auto-created by signal)
                try:
                    profile = user.profile
                    profile.bio = user_data['bio']
                    profile.location = user_data['location']
                    # Randomly set some profile fields
                    profile.show_email = random.choice([True, False])
                    profile.show_birth_date = random.choice([True, False])
                    profile.save()
                except Profile.DoesNotExist:
                    # Create profile if signal didn't work
                    Profile.objects.create(
                        user=user,
                        bio=user_data['bio'],
                        location=user_data['location'],
                        show_email=random.choice([True, False]),
                        show_birth_date=random.choice([True, False])
                    )
                
                # Ensure user settings exist (get_or_create handles signal conflicts)
                settings, created = UserSettings.objects.get_or_create(
                    user=user,
                    defaults={
                        'profile_visibility': random.choice(['public', 'friends', 'private']),
                        'default_post_privacy': random.choice(['public', 'friends', 'private']),
                        'allow_friend_requests': True,
                        'email_notifications': random.choice([True, False]),
                        'notify_friend_requests': True,
                    }
                )
                
                # If settings already existed (from signal), update some fields
                if not created:
                    settings.profile_visibility = random.choice(['public', 'friends', 'private'])
                    settings.default_post_privacy = random.choice(['public', 'friends', 'private'])
                    settings.email_notifications = random.choice([True, False])
                    settings.save()
                
                created_users.append(user)
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user.username} ({user.first_name} {user.last_name})')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {len(created_users)} users!')
        )
        self.stdout.write(
            self.style.WARNING('\nTest users login credentials:')
        )
        self.stdout.write(
            self.style.WARNING('Username: [any of the created usernames]')
        )
        self.stdout.write(
            self.style.WARNING('Password: testpass123')
        )
        
        if created_users:
            self.stdout.write(
                self.style.SUCCESS(f'\nCreated users: {", ".join([u.username for u in created_users])}')
            )
