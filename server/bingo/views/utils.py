from django.conf import settings
import math
from rest_framework import status
from rest_framework.response import Response
from ..models import TileInteraction, Friendship
from ..serializers import FriendshipUserSerializer


def check_access(current_user, target_user):
    """
    Profile visibility levels:
      - 0 (staff-only): Only staff members can view.
      - 1 (friends-only): Viewable by staff and friends.
      - 2 (public): Viewable by anyone, including non-logged-in users.

    Conditions for access:
      1. Staff members can view any profile.
      2. Users can view their own profile.
      3. Friends can view each others' profile except staff-only.
      4. Public profiles (visibility=2) are accessible to everyone.
    """
    # Staff members and the profile owner can always view the profile.
    if current_user.is_staff or current_user == target_user:
        return True

    # Check if `current_user` and `target_user` are friends.
    elif (current_user.is_authenticated and
          (Friendship.objects.filter(requester=current_user, receiver=target_user, status=Friendship.ACCEPTED).exists() or
           Friendship.objects.filter(requester=target_user, receiver=current_user, status=Friendship.ACCEPTED).exists())):
        return target_user.visibility != 0

    # Public profiles (visibility=2) are accessible to everyone.
    return target_user.visibility == 2


def check_bingo(tile):
    # Every tile that relates to this user/grid combo.
    all_tiles = TileInteraction.objects.filter(user=tile.user, grid=tile.grid)

    # Size of the bingo grid.
    grid_size = 16
    grid_width = int(math.sqrt(grid_size))
    completion_grid = grid_size*[0]

    # One-dimensional array to represent the bingo grid, and completion of the challenges.
    for t in all_tiles:
        completion_grid[t.position] = 1 if t.completed else 0
    # Coordinates of the tile.
    tile_row = tile.position // grid_width
    tile_col = tile.position % grid_width
    bingos = {'bingo_row': -1,
              'bingo_col': -1,
              'bingo_diag': -1,
              'full_bingo': False,
              'bingo_points': 0}

    # Helper function for checking a bingo in a line/diagonal
    def check_line(indices):
        return all(completion_grid[i] for i in indices)

    # Check the row for bingo.
    row_indices = range(tile_row*grid_width, tile_row*grid_width+grid_width)
    if check_line(row_indices):
        bingos['bingo_row'] = tile_row
        bingos['bingo_points'] += settings.BINGO_COMPLETE

    # Check the column for bingo.
    col_indices = range(tile_col, grid_size, grid_width)
    if check_line(col_indices):
        bingos['bingo_col'] = tile_col
        bingos['bingo_points'] += settings.BINGO_COMPLETE

    # If the tile exists in a diagonal, check the diagonal for bingos.
    if tile_row == tile_col:
        # This diagonal goes top left to bottom right.
        diag1_indices = range(0, grid_size, grid_width+1)
        if check_line(diag1_indices):
            bingos['bingo_diag'] = 0
            bingos['bingo_points'] += settings.BINGO_COMPLETE
    if tile_row + tile_col == grid_width - 1:
        # This diagonal goes bottom left to top right.
        diag2_ranges = range(grid_width - 1, grid_size - 1, grid_width - 1)
        if check_line(diag2_ranges):
            bingos['bingo_diag'] = 3
            bingos['bingo_points'] += settings.BINGO_COMPLETE

    if len(all_tiles) == grid_size:
        # Check for full bingo
        if all(completion_grid):
            bingos['full_bingo'] = True
            bingos['bingo_points'] += settings.GRID_COMPLETE
    return bingos


def check_friendships(user_set, current_user):
    list_out = []
    for user in user_set:
        # Skip if this is the current user
        if user['user_id'] == current_user.user_id:
            continue
        # Check if current user is requester
        friendship = get_or_none(Friendship, requester=current_user, receiver=user['user_id'])
        if friendship:
            if friendship.status == friendship.PENDING:
                list_out.append(
                    {'user_data': user, 'status': 'You have requested friendship.'})
            elif friendship.status == friendship.ACCEPTED:
                list_out.append(
                    {'user_data': user, 'status': 'You are friends.'})
        # Check if current user is receiver
        elif (friendship := get_or_none(Friendship, requester=user['user_id'], receiver=current_user)) is not None:
            if friendship.status == friendship.PENDING:
                list_out.append(
                    {'user_data': user, 'status': 'Pending friendship request.', 'friendship_id': friendship.id})
            elif friendship.status == friendship.ACCEPTED:
                list_out.append(
                    {'user_data': user, 'status': 'You are friends.'})
        else:
            list_out.append(
                {'user_data': user, 'status': 'You are not friends.'})
    return list_out


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


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
    # Prepare the response data
    result = []
    for friendship in friendships:
        # Get the friend (either requester or receiver)
        friend = getattr(friendship, 'receiver' if is_outgoing else 'requester')
        # Create serializer with friendship context
        serializer = FriendshipUserSerializer(
            friend,
            context={'friendship': friendship}
        )
        result.append(serializer.data)
    return Response(result, status=status.HTTP_200_OK)
