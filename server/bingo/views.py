from .serializers import UserRegisterSerializer, UserProfileSerializer
from django.shortcuts import render  # noqa
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Friendship
from django.db.models import Q  



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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friends(request):
    """
    Get all accepted friends of the logged-in user.
    Requires authentication.
    """
    # Get all accepted friendships where user is either requester or receiver
    friendships = Friendship.objects.filter(
        status='accepted'
    ).filter(
        Q(requester=request.user) | Q(receiver=request.user)
    )
    
    # Get the corresponding friend users
    friend_users = []
    for friendship in friendships:
        friend = (friendship.receiver if friendship.requester == request.user 
                 else friendship.requester)
        friend_users.append(friend)
    
    serializer = UserProfileSerializer(friend_users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outgoing_requests(request):
    """
    Get all outgoing friend requests of the logged-in user.
    Requires authentication.
    """
    # Get pending friendships where user is the requester
    friendships = Friendship.objects.filter(
        status='pending',
        requester=request.user
    )
    
    # Get the users who received the requests
    friend_users = [friendship.receiver for friendship in friendships]
    
    serializer = UserProfileSerializer(friend_users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_incoming_requests(request):
    """
    Get all incoming friend requests to the logged-in user.
    Requires authentication.
    """
    # Get pending friendships where user is the receiver
    friendships = Friendship.objects.filter(
        status='pending',
        receiver=request.user
    )
    
    # Get the users who sent the requests
    friend_users = [friendship.requester for friendship in friendships]
    
    serializer = UserProfileSerializer(friend_users, many=True)
    return Response(serializer.data)