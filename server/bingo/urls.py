from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from bingo import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register_user, name='register_user'),
    path('leaderboard/', views.get_leaderboard, name='get_leaderboard'),
    path('user/me/', views.get_current_user, name='current-user'),
    path('delete-friendship/<int:friendship_id>/', views.delete_friendship, name='delete_friendship'),
    path('friends/', views.get_friends, name='friend-list'),
    path('friends/requests/outgoing/', views.get_outgoing_requests, name='outgoing-requests'),
    path('friends/requests/incoming/', views.get_incoming_requests, name='incoming-requests'),
    path('accept-friendship/<int:friendship_id>/', views.accept_friendship, name='accept_friendship'),
]
