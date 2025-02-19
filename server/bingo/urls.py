from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from bingo.views import bingo_views, friends_views, leaderboard_views, user_views, email_views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', user_views.register_user, name='register_user'),
    path('update-preferences/', user_views.update_user_preferences, name='update_preferences'),
    path('leaderboard/', leaderboard_views.get_leaderboard, name='get_leaderboard'),
    path('user/me/', user_views.get_current_user, name='current_user'),
    path('delete-friendship/<int:friendship_id>/', friends_views.delete_friendship, name='delete_friendship'),
    path('start-challenge/', bingo_views.start_challenge, name="start_challenge"),
    path('friends/all/', friends_views.get_all_friends_data, name='all_friends_data'),
    path('bingo-grid/', bingo_views.get_bingo_grid, name='get_bingo_grid'),
    path('accept-friendship/<int:friendship_id>/', friends_views.accept_friendship, name='accept_friendship'),
    path('get-profile-page/<str:username>/', user_views.get_profile_page, name='get_profile_page'),
    path('complete-challenge/', bingo_views.complete_challenge, name='complete_challenge'),
    path('request-friendship/<int:user_id>/', friends_views.request_friendship, name='request_friendship'),
    path('user-search/', user_views.find_user, name='user_search'),
    path('update-bingo-grid/', bingo_views.update_bingo_grid, name='update-bingo-grid'),
    path("email-validation/", email_views.request_email_verification, name='request_verification'),
    path("activate/", email_views.confirm_email, name="confirm_email"),
    path("request-reset/", email_views.request_password_reset, name="request_password_reset"),
    path("reset-password/", email_views.reset_password, name="reset_password"),
]
