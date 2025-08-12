from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.user_search_view, name='user_search'),
    path('send-friend-request/<int:user_id>/', views.send_friend_request_view, name='send_friend_request'),
    path('accept-friend-request/<int:friendship_id>/', views.accept_friend_request_view, name='accept_friend_request'),
    path('decline-friend-request/<int:friendship_id>/', views.decline_friend_request_view, name='decline_friend_request'),
]
