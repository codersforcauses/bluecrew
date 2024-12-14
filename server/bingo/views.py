from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',       # maps to userId
            'username',      # maps to userName
            'first_name',    # maps to firstName
            'last_name',     # maps to lastName
            'bio',
            'total_points',  # maps to totalPoints
            'email',
            'visibility',
            'avatar'
        ]

    def to_representation(self, instance):
        # This ensures the field names match the TypeScript interface
        data = super().to_representation(instance)
        return {
            'userId': data['user_id'],
            'userName': data['username'],
            'firstName': data['first_name'],
            'lastName': data['last_name'],
            'bio': data['bio'],
            'totalPoints': data['total_points'],
            'email': data['email'],
            'visibility': data['visibility'],
            'avatar': data['avatar']
        }

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Get details of currently logged in user.
    Requires authentication.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)