from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import User
from ..serializers import (UpdatePreferencesSerializer, UserProfileSerializer,
                           UserRegisterSerializer, UserSearchSerializer)
from .utils import check_friendships


@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'User created successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def get_current_user(request):
    """
    Get details of currently logged in user.
    Requires authentication.
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated, ))
def update_user_preferences(request):
    serializer = UpdatePreferencesSerializer(
        instance=request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def find_user(request):
    """
    This view will return a set of users whose usernames begin with a given string.
    The number of users returned is equal to USERS_RETURNED
    The view requires 1 argument 'query_string' which is the string that the search will be performed with.
    The view returns a list of dictionaries in the form:
    [{'user_data': {'avatar': int, 'username': str, 'user_id': int},
      'status': friendship_message, 'friendship_id': friendship.id}, ...]
    friendship_message are either: 'You are friends.', 'You are not friends.', 'You've requested friendship.',
    or 'Pending friendship request.'
    """
    USERS_RETURNED = 15
    try:
        query_string = request.data['query_string']
    except KeyError:
        return Response({'error': 'Field "query_string" is required in this request'},
                        status=status.HTTP_400_BAD_REQUEST)

    user_set = User.objects.filter(
        username__istartswith=query_string, is_active=True, is_superuser=False).order_by('username')[:USERS_RETURNED]
    serializer = UserSearchSerializer(user_set, many=True)
    response = check_friendships(serializer.data, request.user)
    return Response(response, status=status.HTTP_200_OK)
