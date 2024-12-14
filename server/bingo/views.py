from django.shortcuts import render  # noqa
from .models import Friendship
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_friendship(request, friendship_id):
    try:
        friendship = Friendship.objects.get(id=friendship_id)

        if request.user != friendship.requester and request.user != friendship.receiver:
            return Response({"error": "You do not have permission to delete this friendship."}, status=403)

        friendship.delete()
        return Response({"message": "Friendship deleted successfully."}, status=204)

    except Friendship.DoesNotExist:
        return Response({"error": "Friendship not found."}, status=404)
