from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import ChallengeInteraction, Challenge


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
    challenge = Challenge.objects.filter(id=request.data["challenge"])

    # Complain if the specified challenge doesn't exist (or if there's somehow more than one)
    if len(challenge) != 1:
        return Response(status=status.HTTP_409_CONFLICT)

    challenge = challenge[0]

    interactions = ChallengeInteraction.objects.filter(user=request.user, challenge=challenge)
    # Throw an error if there is already an interaction between that user and that challenge
    if len(interactions) != 0:
        return Response(status=status.HTTP_409_CONFLICT)

    interaction = ChallengeInteraction.objects.create(user=request.user, challenge=challenge)
    interaction.save()
    return Response(status=status.HTTP_200_OK)
