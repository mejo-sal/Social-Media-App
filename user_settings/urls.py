from django.urls import path
from . import views

app_name = 'user_settings'

urlpatterns = [
    path('settings/edit/', views.edit_user_settings, name='edit_settings'),
]
