from rest_framework import status, permissions
from .serializers import UserRegisterSerializer, UserProfileSerializer, LeaderboardUserSerializer, BingoGridSerializer
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Friendship, User, BingoGrid, TileInteraction
from django.db import IntegrityError
from django.db.models import Q, F, Window
from django.db.models.functions import DenseRank


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_challenge(request):
    try:
        challenge_index = int(request.data["position"])
    except ValueError:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if challenge_index not in range(16):
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    try:
        grid = BingoGrid.objects.get(is_active=True)
    except ObjectDoesNotExist:
        # Throw an error if no grid is currently active
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        TileInteraction.objects.create(user=request.user, position=challenge_index, grid=grid)
    except IntegrityError:
        # Throw an error if there is already an interaction between that user and that challenge
        return Response(status=status.HTTP_409_CONFLICT)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
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
        friend = (friendship.receiver if friendship.requester ==
                  request.user else friendship.requester)
        friend_users.append(friend)
    serializer = UserProfileSerializer(friend_users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def get_outgoing_requests(request):
    """Get all outgoing friend requests of the logged-in user.
    Requires authentication."""
    return get_friend_requests(request, is_outgoing=True)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def get_incoming_requests(request):
    """Get all incoming friend requests to the logged-in user.
    Requires authentication."""
    return get_friend_requests(request, is_outgoing=False)


@api_view(['GET'])
def get_leaderboard(request):
    """
    Returns a leaderboard of size 'leaderboard_size'.
    The current user's rank is also added to the end of the leaderboard, regardless of rank.
    If the current user has a place in the leaderboard, they will appear twice - in the leaderboard and at the end.
    """
    # Size of the leaderboard returned, excluding the current user.
    logged_in = request.user.is_authenticated
    leaderboard_size = 20
    user_set = User.objects.all()
    if not user_set:
        return Response({'No users found in database.'}, status=status.HTTP_200_OK)
    # Annotate the user query set with each user's respective rank.
    user_set = user_set.annotate(
        rank=Window(
            expression=DenseRank(),
            order_by=F('total_points').desc(),
        )
    )
    serializer = LeaderboardUserSerializer(
        user_set, many=True)
    leaderboard = []
    current_user_index = -1
    user_found = False
    for i in range(len(serializer.data)):
        # Check for current user.
        if logged_in:
            if user_set[i].username == str(request.user):
                current_user_index = i
                user_found = True
            # If checking indices over the leaderboard_size, skip any users that are not the current user.
        if i >= leaderboard_size:
            # End search if leaderboard is populated, and the current user's rank is found.
            if user_found or not logged_in:
                break
        else:
            # Add annotated rank field to serializer.
            serializer.data[i]['rank'] = user_set[i].rank
            leaderboard.append(serializer.data[i])
    # Append current user to end of leaderboard.
    if logged_in:
        leaderboard.append(serializer.data[current_user_index])
    return Response(leaderboard, status=status.HTTP_200_OK)


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
def get_bingo_grid(request):
    """
    This view returns a dictionary with two keys.
    'grid_id' contains the pk of the active bingo grid.
    'challenges' contains a list of 16 dictionaries, 1 for each challenge.
    Each challenge dictionary contains the 'name', 'description', 'challenge_type', and 'points' of the challenge.
    If the user is authenticated, then each challenge dictionary will also contain the 'status' of completion
    for that user.
    """
    # Fetch the currently active bingo grid.
    active_grid = get_object_or_404(BingoGrid, is_active=True)
    # Serialized form of object
    grid = BingoGridSerializer(active_grid).data

    logged_in = request.user.is_authenticated
    if logged_in:
        # Find all tiles of the active bingo grid that the user has interacted with.
        user_interaction = TileInteraction.objects.filter(
            user=request.user, grid=active_grid)
        # By default, a tile will not have been started.
        for chal in grid['challenges']:
            chal['status'] = "Not Started"
        # If a user interaction exists with a tile, change its completion status accordingly
        if user_interaction:
            for tile in user_interaction:
                grid['challenges'][tile.position]['status'] = 'Completed' if tile.completed else 'Started'
    return Response(grid, status=status.HTTP_200_OK)
