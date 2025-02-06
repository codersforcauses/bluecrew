from django.db.models.functions import DenseRank
from django.db.models import F, Window
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import User
from ..serializers import LeaderboardUserSerializer


@api_view(['GET'])
def get_leaderboard(request):
    """
    Returns a leaderboard of size 'leaderboard_size', excluding superusers.
    The current user's rank is also added to the end of the leaderboard, regardless of rank.
    If the current user has a place in the leaderboard, they will appear twice - in the leaderboard and at the end.
    """
    logged_in = request.user.is_authenticated
    leaderboard_size = 20

    # Filter out superusers/inactive users and get base queryset
    user_set = User.objects.filter(is_superuser=False, is_active=True)
    if not user_set:
        return Response({'No users found in database.'}, status=status.HTTP_200_OK)

    # Annotate ranks
    user_set = user_set.annotate(
        rank=Window(
            expression=DenseRank(),
            order_by=F('total_points').desc(),
        )
    )

    serializer = LeaderboardUserSerializer(user_set, many=True)
    leaderboard = []
    current_user_index = -1

    # Process users
    for i in range(len(serializer.data)):
        # Only look for current user if they're logged in and not a superuser
        if logged_in and not request.user.is_superuser:
            if user_set[i].username == str(request.user):
                current_user_index = i

        # Add users to leaderboard up to leaderboard_size
        if i < leaderboard_size:
            serializer.data[i]['rank'] = user_set[i].rank
            leaderboard.append(serializer.data[i])

    # Always append current user to end of leaderboard if they're logged in and not a superuser
    if logged_in and not request.user.is_superuser and current_user_index != -1:
        current_user_data = serializer.data[current_user_index]
        current_user_data['rank'] = user_set[current_user_index].rank
        leaderboard.append(current_user_data)

    return Response(leaderboard, status=status.HTTP_200_OK)
