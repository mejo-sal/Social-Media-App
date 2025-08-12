from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserSettings
from .forms import UserSettingsForm


@login_required
def user_settings_view(request):
    """User settings view"""
    # Get or create user settings
    settings, created = UserSettings.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings have been updated successfully.')
            return redirect('user_settings')
    else:
        form = UserSettingsForm(instance=settings)
    
    return render(request, 'user_settings/settings.html', {
        'form': form,
        'settings': settings
    })
