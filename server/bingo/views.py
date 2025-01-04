from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import ChallengeInteraction


@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'User created successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Get details of currently logged in user.
    Requires authentication.
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_challenge(request):
    interactions = ChallengeInteraction.objects.filter(user=request.user, challenge=request.challenge)
    if len(interactions) != 0:
        return Response(status=status.HTTP_409_CONFLICT)

    interaction = ChallengeInteraction(user=request.user, challenge=request.challenge)
    interaction.save()
    return Response(status=status.HTTP_200_OK)
