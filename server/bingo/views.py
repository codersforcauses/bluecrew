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
