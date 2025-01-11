from .serializers import UserRegisterSerializer, UserProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import ChallengeInteraction, Challenge, Friendship
from rest_framework.response import Response
from django.db.models import Q


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_friendship(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id)
    if request.user not in {friendship.requester, friendship.receiver}:
        return Response(
            {"error": "You do not have permission to delete this friendship."},
            status=status.HTTP_403_FORBIDDEN
        )
    friendship.delete()
    return Response({"message": "Friendship deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


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
    """Get details of currently logged in user.
    Requires authentication."""
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friends(request):
    """Get all accepted friends of the logged-in user.
    Requires authentication."""
    friendships = Friendship.objects.filter(
        status='accepted'
    ).filter(
        Q(requester=request.user) | Q(receiver=request.user)
    )
    friend_users = []
    for friendship in friendships:
        friend = (friendship.receiver if friendship.requester == request.user else friendship.requester)
        friend_users.append(friend)
    serializer = UserProfileSerializer(friend_users, many=True)
    return Response(serializer.data)


def get_friend_requests(request, is_outgoing=True):
    """Helper function to get friend requests.
    Args:
        request: The HTTP request
        is_outgoing: If True, get outgoing requests; if False, get incoming
    """
    filter_kwargs = {
        'status': 'pending',
        'requester' if is_outgoing else 'receiver': request.user
    }
    friendships = Friendship.objects.filter(**filter_kwargs)
    friend_users = [
        getattr(friendship, 'receiver' if is_outgoing else 'requester') for friendship in friendships
    ]
    serializer = UserProfileSerializer(friend_users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outgoing_requests(request):
    """Get all outgoing friend requests of the logged-in user.
    Requires authentication."""
    return get_friend_requests(request, is_outgoing=True)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_incoming_requests(request):
    """Get all incoming friend requests to the logged-in user.
    Requires authentication."""
    return get_friend_requests(request, is_outgoing=False)
