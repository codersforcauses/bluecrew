from rest_framework import status
from rest_framework.decorators import api_view
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
def get_leaderboard(request):
    leaderboard_size = 20
    leaderboard = User.objects.all()[:leaderboard_size]
    leaderboard = leaderboard.annotate(
        rank=Window(
            expression=DenseRank(),
            order_by=F('total_points').desc(),
        )
    )
    serializer = LeaderboardUserSerializer(leaderboard, many=True)
    for i in range(len(serializer.data)):
        serializer.data[i]['rank'] = leaderboard[i].rank

    return Response(serializer.data)
