from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_settings_view, name='user_settings'),
]
