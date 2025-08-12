from django import forms
from .models import UserSettings


class UserSettingsForm(forms.ModelForm):
    """Form for updating user settings and preferences"""
    
    class Meta:
        model = UserSettings
        fields = [
            'profile_visibility',
            'default_post_privacy',
            'allow_friend_requests',
            'show_email',
            'show_birth_date',
            'email_notifications',
            'notify_friend_requests',
        ]
        widgets = {
            'profile_visibility': forms.Select(attrs={
                'class': 'form-select'
            }),
            'default_post_privacy': forms.Select(attrs={
                'class': 'form-select'
            }),
            'allow_friend_requests': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'show_email': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'show_birth_date': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notify_friend_requests': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add help text as descriptions
        self.fields['profile_visibility'].help_text = "Control who can see your profile"
        self.fields['default_post_privacy'].help_text = "Default privacy setting for new posts"
        self.fields['allow_friend_requests'].help_text = "Allow others to send you friend requests"
        self.fields['show_email'].help_text = "Display your email address on your profile"
        self.fields['show_birth_date'].help_text = "Display your birth date on your profile"
        self.fields['email_notifications'].help_text = "Receive notifications via email"
        self.fields['notify_friend_requests'].help_text = "Get notified when someone sends you a friend request"
