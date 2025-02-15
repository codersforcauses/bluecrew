from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from bingo.views import (bingo_views, friends_views, leaderboard_views,
                         user_views,)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', user_views.register_user, name='register_user'),
    path('update-preferences/', user_views.update_user_preferences,
         name='update_preferences'),
    path('leaderboard/', leaderboard_views.get_leaderboard, name='get_leaderboard'),
    path('user/me/', user_views.get_current_user, name='current_user'),
    path('delete-friendship/<int:friendship_id>/',
         friends_views.delete_friendship, name='delete_friendship'),
    path('start-challenge/', bingo_views.start_challenge, name="start_challenge"),
    path('friends/', friends_views.get_friends, name='friend_list'),
    path('friends/requests/outgoing/',
         friends_views.get_outgoing_requests, name='outgoing_requests'),
    path('friends/requests/incoming/',
         friends_views.get_incoming_requests, name='incoming_requests'),
    path('bingo-grid/', bingo_views.get_bingo_grid, name='get_bingo_grid'),
    path('accept-friendship/<int:friendship_id>/',
         friends_views.accept_friendship, name='accept_friendship'),
    path('get-profile-page/<str:username>/',
         user_views.get_profile_page, name='get_profile_page'),
    path('complete-challenge/', bingo_views.complete_challenge,
         name='complete_challenge'),
    path('request-friendship/<int:user_id>/',
         friends_views.request_friendship, name='request_friendship'),
    path('user-search/', user_views.find_user, name='user_search'),
    path('friends/all/', friends_views.get_all_friends_data, name='all_friends_data'),
]
