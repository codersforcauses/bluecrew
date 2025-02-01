from .utils import check_bingo, check_access
from django.utils import timezone
from django.db.models.functions import DenseRank
from django.db.models import Q, F, Window
from django.db import IntegrityError
from .models import Friendship, User, BingoGrid, TileInteraction
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from .serializers import (UserRegisterSerializer, UserProfileSerializer,
                          LeaderboardUserSerializer, BingoGridSerializer,
                          UpdatePreferencesSerializer, ChallengeCompleteSerializer,
                          ProfilePageChallengeSerializer, ProfilePageSerializer,
                          ProfilePageTileSerializer)


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


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_preferences(request):
    serializer = UpdatePreferencesSerializer(
        instance=request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        TileInteraction.objects.create(
            user=request.user, position=challenge_index, grid=grid)
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
    Returns a leaderboard of size 'leaderboard_size', excluding superusers.
    The current user's rank is also added to the end of the leaderboard, regardless of rank.
    If the current user has a place in the leaderboard, they will appear twice - in the leaderboard and at the end.
    """
    logged_in = request.user.is_authenticated
    leaderboard_size = 20

    # Filter out superusers and get base queryset
    user_set = User.objects.filter(is_superuser=False)
    if not user_set:
        return Response({'No users found in database.'}, status=status.HTTP_200_OK)

    # Annotate ranks
    user_set = user_set.annotate(
        rank=Window(
            expression=DenseRank(),
            order_by=F('total_points').desc(),
        )
    )

    serializer = LeaderboardUserSerializer(user_set, many=True)
    leaderboard = []
    current_user_index = -1

    # Process users
    for i in range(len(serializer.data)):
        # Only look for current user if they're logged in and not a superuser
        if logged_in and not request.user.is_superuser:
            if user_set[i].username == str(request.user):
                current_user_index = i

        # Add users to leaderboard up to leaderboard_size
        if i < leaderboard_size:
            serializer.data[i]['rank'] = user_set[i].rank
            leaderboard.append(serializer.data[i])

    # Always append current user to end of leaderboard if they're logged in and not a superuser
    if logged_in and not request.user.is_superuser and current_user_index != -1:
        current_user_data = serializer.data[current_user_index]
        current_user_data['rank'] = user_set[current_user_index].rank
        leaderboard.append(current_user_data)

    return Response(leaderboard, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def request_friendship(request, user_id):
    receiver = get_object_or_404(User, user_id=user_id)

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


@api_view(['GET'])
def get_profile_page(request, username):
    try:
        target_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user_info = ProfilePageSerializer(target_user).data

    if not check_access(request.user, target_user):
        return Response({"user_info": user_info, "challenges": []}, status=status.HTTP_200_OK)

    target_tiles = TileInteraction.objects.filter(user=target_user)
    target_challenges = [list(tile.grid.challenges.all())[
        tile.position] for tile in target_tiles]

    tiles_data = ProfilePageTileSerializer(target_tiles, many=True).data
    challenges_data = (ProfilePageChallengeSerializer(
        target_challenges, many=True).data)
    challenges_tiles_data = [{**tile_data, **challenge_data}
                             for tile_data, challenge_data in zip(tiles_data, challenges_data)]

    response_data = {
        "user_info": user_info,
        "challenges": challenges_tiles_data
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes((permissions.IsAuthenticated, ))
def complete_challenge(request):
    """
    This view returns a dictionary the following information.
    'challenge_points' contains the points earned from completing the challenge.
    'bingo_points' contains the points earned from bingos completed
    'bingo_rows' contains the row in which a bingo was just achieved, if any, from 0-3, -1 if no bingo
    'bingo_cols' contains the column in which a bingo was just achieved, if any, from 0-3, -1 if no bingo
    'bingo_diag' contains the diagonal in which a bingo was just achieved, if any, denoted by the first row
    tile the diagonal contains, either 0 or 3, -1 if no bingo.
    'full_bingo' contains a boolean, representing whether the full grid has been completed.
    """
    try:
        active_grid = BingoGrid.objects.get(is_active=True)
    except BingoGrid.DoesNotExist:
        return Response(
            {"message": "No bingo grid found. Please contact support."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    serializer = ChallengeCompleteSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    tile = get_object_or_404(TileInteraction, user=request.user,
                             grid=active_grid, position=serializer.validated_data['position'])

    # Update consent and image fields.
    tile.consent = serializer.validated_data['consent']
    tile.image = serializer.validated_data['image']

    # Points should only be awarded once.
    if tile.completed:
        return Response({'error': 'Challenge has already been completed for this user.'}, status=status.HTTP_409_CONFLICT)

    tile.completed = True
    tile.date_completed = timezone.now()
    tile.save()

    challenge = active_grid.challenges.all()[tile.position]
    challenge.total_completions += 1
    challenge.save()

    user = request.user
    user.total_points += challenge.points
    user.save()

    bingos = check_bingo(tile)
    response = {'challenge_points': challenge.points}
    response.update(bingos)

    return Response(response, status.HTTP_200_OK)
