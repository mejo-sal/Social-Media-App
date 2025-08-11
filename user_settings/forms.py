from django import forms

class UserSettingsForm(forms.Form):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends Only'),
        ('private', 'Private'),
    ]

    profile_visibility = forms.ChoiceField(choices=PRIVACY_CHOICES, initial='public')
    default_post_privacy = forms.ChoiceField(choices=PRIVACY_CHOICES, initial='public')
    allow_friend_requests = forms.BooleanField(required=False, initial=True)
    show_email = forms.BooleanField(required=False, initial=False)
    show_birth_date = forms.BooleanField(required=False, initial=True)
    email_notifications = forms.BooleanField(required=False, initial=True)
    notify_friend_requests = forms.BooleanField(required=False, initial=True)
    two_factor_enabled = forms.BooleanField(required=False, initial=False)
