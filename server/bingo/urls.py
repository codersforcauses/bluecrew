from django.urls import path
from bingo.views import delete_friendship

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from bingo import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register_user, name='register_user'),
    path('user/me/', views.get_current_user, name='current-user'),
    path('delete-friendship/<int:friendship_id>/',
         delete_friendship, name='delete_friendship'),
]
