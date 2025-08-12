# SocialHub - Django Social Media Application

A full-featured social media application built with Django, featuring user authentication, profiles, posts, friend requests, notifications, and email integration.

## Features

- **User Authentication & Profiles**
  - User registration and login
  - Extended user profiles with avatars, bio, and location
  - Profile editing and management

- **Social Features**
  - Friend request system
  - User search functionality
  - Email notifications for friend requests
  - Real-time notification system

- **User Settings**
  - Privacy controls (profile visibility, post privacy)
  - Notification preferences (email notifications, friend request alerts)
  - Account security settings

- **Notification System**
  - In-app notifications with badge counter
  - Email notifications with beautiful HTML templates
  - Notification filtering and management
  - Mark as read/delete functionality

- **Posts & Interactions** (Framework Ready)
  - Post creation and management
  - Comment system
  - Like/unlike functionality
  - Media upload support

## Technology Stack

- **Backend**: Django 4.2.9, Python 3.x
- **Database**: SQLite (development), PostgreSQL ready
- **Frontend**: Bootstrap 5.1.3, FontAwesome icons
- **Email**: Gmail SMTP integration
- **Media**: Pillow for image processing

## Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Social-Media-App/Social-Media-App
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Seed test users (optional)**
   ```bash
   python manage.py seed_users --count 10
   ```

7. **Create test notifications (optional)**
   ```bash
   python manage.py create_test_notifications --username <your-username> --count 15
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to access the application.

## Test Users

The application comes with pre-configured test users for development and testing purposes. All test users use the password: **`testpass123`**

| First Name | Last Name | Username | Email | Location |
|------------|-----------|----------|-------|----------|
| Alice | Johnson | alice_johnson | alice.johnson@example.com | San Francisco, CA |
| Bob | Smith | bob_smith | bob.smith@example.com | New York, NY |
| Carol | Davis | carol_davis | carol.davis@example.com | Chicago, IL |
| David | Wilson | david_wilson | david.wilson@example.com | Los Angeles, CA |
| Emma | Brown | emma_brown | emma.brown@example.com | Seattle, WA |
| Frank | Taylor | frank_taylor | frank.taylor@example.com | Nashville, TN |
| Grace | Martinez | grace_martinez | grace.martinez@example.com | Austin, TX |
| Henry | Garcia | henry_garcia | henry.garcia@example.com | Miami, FL |
| Isabel | Rodriguez | isabel_rodriguez | isabel.rodriguez@example.com | Portland, OR |
| Jack | Lee | jack_lee | jack.lee@example.com | San Jose, CA |

**Note**: All test users have the same password: `testpass123`

## Email Configuration

To enable email notifications, update the email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

## Project Structure

```
Social-Media-App/
├── accounts/           # User authentication and profiles
├── core/              # Friendship system and core functionality
├── notifications/     # Notification system and email logs
├── posts/            # Posts, comments, and likes (framework ready)
├── search/           # Search functionality
├── user_settings/    # User privacy and notification settings
├── templates/        # HTML templates
├── static/          # CSS, JS, and media files
└── socialhub/       # Main project settings
```

## Key URLs

- `/` - Home (redirects to login if not authenticated)
- `/accounts/login/` - User login
- `/accounts/register/` - User registration
- `/accounts/profile/` - User profile
- `/friends/` - Friend search and management
- `/notifications/` - Notification center
- `/settings/` - User settings
- `/admin/` - Django admin interface

## Management Commands

### Seed Test Users
```bash
python manage.py seed_users --count 10
```

### Create Test Notifications
```bash
python manage.py create_test_notifications --username <username> --count 15
```

## Database Schema

The application uses a comprehensive database schema supporting:
- User authentication and extended profiles
- Friend request system with status tracking
- Notification system with email logging
- User settings and privacy controls
- Posts and interactions framework

See `facebook_clone_schema.dbml` for detailed database schema documentation.

## Development Features

- **Email Templates**: Beautiful HTML email templates for notifications
- **AJAX Support**: Dynamic UI updates without page refresh
- **Responsive Design**: Mobile-friendly Bootstrap interface
- **Security**: CSRF protection, user authentication, and authorization
- **Scalable**: Modular Django app structure for easy extension

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is for educational purposes and learning Django development.

---

**Built with ❤️ using Django**