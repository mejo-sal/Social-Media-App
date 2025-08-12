from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
]
