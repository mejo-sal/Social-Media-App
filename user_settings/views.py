from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserSettingsForm
from .models import UserSettings
@login_required
def edit_user_settings(request):
    user = request.user
    try:
        settings = user.settings
    except UserSettings.DoesNotExist:
        settings = UserSettings(user=user)
    
    if request.method == 'POST':
        form = UserSettingsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            settings.profile_visibility = data['profile_visibility']
            settings.default_post_privacy = data['default_post_privacy']
            settings.allow_friend_requests = data['allow_friend_requests']
            settings.show_email = data['show_email']
            settings.show_birth_date = data['show_birth_date']
            settings.email_notifications = data['email_notifications']
            settings.notify_friend_requests = data['notify_friend_requests']
            settings.two_factor_enabled = data['two_factor_enabled']
            settings.save()
            return redirect('profile')
    else:
        # هنا الفورم بيتعرف فقط في حالة GET مع البيانات الأولية
        initial_data = {
            'profile_visibility': settings.profile_visibility,
            'default_post_privacy': settings.default_post_privacy,
            'allow_friend_requests': settings.allow_friend_requests,
            'show_email': settings.show_email,
            'show_birth_date': settings.show_birth_date,
            'email_notifications': settings.email_notifications,
            'notify_friend_requests': settings.notify_friend_requests,
            'two_factor_enabled': settings.two_factor_enabled,
        }
        form = UserSettingsForm(initial=initial_data)


    return render(request, 'user_settings/edit_settings.html', {'form': form})
