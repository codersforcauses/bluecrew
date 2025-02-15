from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import Friendship, User
from ..serializers import FriendshipUserSerializer


@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated, ))
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
@permission_classes((permissions.IsAuthenticated, ))
def request_friendship(request, user_id):
    receiver = get_object_or_404(User, user_id=user_id)
    if not receiver.is_active:
        return Response({'error': 'This user is not active - no friend request was sent.'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        new_friendship = Friendship(
            requester=request.user, receiver=receiver, status=Friendship.PENDING)
        new_friendship.full_clean()
        new_friendship.save()
        return Response(
            {"message": "Friendship request sent successfully."},
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        error_message = e.message_dict.get('__all__', ['Validation error'])[0]
        if "already exists" in error_message or "reverse friendship" in error_message:
            return Response({"error": error_message}, status=status.HTTP_409_CONFLICT)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
        return Response(
            {"error": "A friendship request already exists or is pending."},
            status=status.HTTP_409_CONFLICT
        )


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def accept_friendship(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id)

    if request.user != friendship.receiver:
        return Response(
            {"error": "You do not have permission to accept this friendship."},
            status=status.HTTP_403_FORBIDDEN
        )

    if friendship.status == Friendship.ACCEPTED:
        return Response(
            {"message": "Friendship is already accepted."},
            status=status.HTTP_200_OK
        )

    if friendship.status != Friendship.ACCEPTED:
        friendship.status = Friendship.ACCEPTED
        friendship.save()
        return Response(
            {"message": "Friendship accepted successfully."},
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def get_all_friends_data(request):
    """Get all friends data including current friends, incoming and outgoing requests in a single request.
    Requires authentication."""
    # Get all friendships
    all_friendships = Friendship.objects.filter(
        Q(requester=request.user) | Q(receiver=request.user)
    )
    # Get accepted friendships
    accepted_friendships = all_friendships.filter(status=Friendship.ACCEPTED)
    current_friends = []
    for friendship in accepted_friendships:
        friend = (friendship.receiver if friendship.requester == request.user else friendship.requester)
        serializer = FriendshipUserSerializer(
            friend,
            context={'friendship': friendship}
        )
        current_friends.append(serializer.data)

    # Get pending incoming requests
    incoming_friendships = all_friendships.filter(
        status=Friendship.PENDING,
        receiver=request.user
    )
    incoming_requests = []
    for friendship in incoming_friendships:
        serializer = FriendshipUserSerializer(
            friendship.requester,
            context={'friendship': friendship}
        )
        incoming_requests.append(serializer.data)

    # Get pending outgoing requests
    outgoing_friendships = all_friendships.filter(
        status=Friendship.PENDING,
        requester=request.user
    )
    outgoing_requests = []
    for friendship in outgoing_friendships:
        serializer = FriendshipUserSerializer(
            friendship.receiver,
            context={'friendship': friendship}
        )
        outgoing_requests.append(serializer.data)

    return Response({
        "current_friends": current_friends,
        "incoming_requests": incoming_requests,
        "outgoing_requests": outgoing_requests
    }, status=status.HTTP_200_OK)
