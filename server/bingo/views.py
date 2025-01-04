from .serializers import UserRegisterSerializer, UserProfileSerializer
from django.shortcuts import render  # noqa
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Friendship


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_friendship(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id)

    # Check if the requesting user is either the requester or receiver of the friendship
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
    """
    Get details of currently logged in user.
    Requires authentication.
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)
