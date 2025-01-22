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
    path('update-preferences/', views.update_user_preferences,
         name='update_preferences'),
    path('leaderboard/', views.get_leaderboard, name='get_leaderboard'),
    path('user/me/', views.get_current_user, name='current_user'),
    path('delete-friendship/<int:friendship_id>/',
         views.delete_friendship, name='delete_friendship'),
    path('start-challenge/', views.start_challenge, name="start_challenge"),
    path('friends/', views.get_friends, name='friend_list'),
    path('friends/requests/outgoing/',
         views.get_outgoing_requests, name='outgoing_requests'),
    path('friends/requests/incoming/',
         views.get_incoming_requests, name='incoming_requests'),
    path('bingo-grid/', views.get_bingo_grid, name='get_bingo_grid'),
    path('accept-friendship/<int:friendship_id>/',
         views.accept_friendship, name='accept_friendship'),
    path('request-friendship/<int:user_id>/',
         views.request_friendship, name='request_friendship'),
]
