from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, LeaderboardUserSerializer
from .models import User
from django.db.models import F, Window
from django.db.models.functions import DenseRank
# Create your views here.


@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'User created successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def get_leaderboard(request):
    """
    Returns a leaderboard of size 'leaderboard_size'.
    The current user's rank is also added to the end of the leaderboard, regardless of rank.
    If the current user has a place in the leaderboard, they will appear twice - in the leaderboard and at the end.
    """
    # Size of the leaderboard returned, excluding the current user.
    leaderboard_size = 20
    user_set = User.objects.all()
    if not user_set:
        return Response({'No users found in database.'}, status=status.HTTP_200_OK)
    # Annotate the user query set with each user's respective rank.
    user_set = user_set.annotate(
        rank=Window(
            expression=DenseRank(),
            order_by=F('total_points').desc(),
        )
    )
    serializer = LeaderboardUserSerializer(
        user_set, many=True)

    leaderboard = []
    current_user_index = -1
    user_found = False
    for i in range(len(serializer.data)):
        # Check for current user.
        if user_set[i].username == str(request.user):
            current_user_index = i
            user_found = True

        # If checking indices over the leaderboard_size, skip any users that are not the current user.
        if i >= leaderboard_size:
            # End search if leaderboard is populated, and the current user's rank is found.
            if user_found:
                break
        else:
            # Add annotated rank field to serializer.
            serializer.data[i]['rank'] = user_set[i].rank
            leaderboard.append(serializer.data[i])
    # Append current user to end of leaderboard.
    leaderboard.append(serializer.data[current_user_index])
    return Response(leaderboard, status=status.HTTP_200_OK)
