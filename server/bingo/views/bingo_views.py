from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import BingoGrid, TileInteraction
from ..serializers import (
    BingoGridSerializer, ChallengeCompleteSerializer, UpdateBingoGridSerializer)
from .utils import check_bingo


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def start_challenge(request):
    try:
        challenge_index = int(request.data["position"])

        if challenge_index not in range(16):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        grid = BingoGrid.objects.get(is_active=True)

        TileInteraction.objects.create(
            user=request.user, position=challenge_index, grid=grid
        )

    except (ValueError, KeyError):
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except IntegrityError:
        return Response(status=status.HTTP_409_CONFLICT)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_bingo_grid(request):
    """
    This view returns data with the following fields.
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
            chal['status'] = "not started"
        # If a user interaction exists with a tile, change its completion status accordingly
        if user_interaction:
            for tile in user_interaction:
                grid['challenges'][tile.position]['status'] = 'completed' if tile.completed else 'started'
    return Response(grid, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes((permissions.IsAuthenticated, ))
def complete_challenge(request):
    """
    This view returns data with the following fields.
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
    # Add description if provided in the serializer data
    if 'description' in serializer.validated_data:
        tile.description = serializer.validated_data['description']

    # Points should only be awarded once.
    if tile.completed:
        return Response({'error': 'Challenge has already been completed for this user.'}, status=status.HTTP_409_CONFLICT)

    tile.completed = True
    tile.date_completed = timezone.now()
    tile.save()

    challenge = active_grid.challenges.all()[tile.position]
    challenge.total_completions += 1
    challenge.save()

    bingos = check_bingo(tile)
    response = {'challenge_points': challenge.points}
    response.update(bingos)

    user = request.user
    user.total_points += challenge.points + bingos['bingo_points']
    user.save()

    return Response(response, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.IsAdminUser, ))
def update_bingo_grid(request):
    serializer = UpdateBingoGridSerializer(data=request.data)
    if serializer.is_valid():
        old_grids = BingoGrid.objects.filter(is_active=True)
        new_grid = serializer.create(serializer.validated_data)
        for old_grid in old_grids:
            old_grid.is_active = False
            old_grid.save()
        new_grid.is_active = True
        new_grid.save()
        return Response({"message": "Bingo grid successfully updated."}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
