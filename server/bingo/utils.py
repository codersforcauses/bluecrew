from .models import TileInteraction  # noqa
import math
from django.conf import settings


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

    bingo_count = 0
    # Check the row for bingo.
    for i in range(tile_row*grid_width, tile_row*grid_width+grid_width):
        if completion_grid[i] == 1:
            bingo_count += 1
    if bingo_count == 4:
        bingos['bingo_row'] = tile_row
        bingos['bingo_points'] += settings.BINGO_COMPLETE
    bingo_count = 0

    # Check the column for bingo.
    for i in range(tile_col, grid_size, grid_width):
        if completion_grid[i] == 1:
            bingo_count += 1
    if bingo_count == 4:
        bingos['bingo_col'] = tile_col
        bingos['bingo_points'] += settings.BINGO_COMPLETE
    bingo_count = 0

    # If the tile exists in a diagonal, check the diagonal for bingos.
    if tile_row == tile_col:
        # This diagonal goes top left to bottom right.
        for i in range(0, grid_size, grid_width+1):
            if completion_grid[i] == 1:
                bingo_count += 1
        if bingo_count == 4:
            bingos[2] = True
            bingos['bingo_diag'] = 0
            bingos['bingo_points'] += settings.BINGO_COMPLETE
        bingo_count = 0
    elif tile_row + tile_col == grid_width - 1:
        # This diagonal goes bottom left to top right.
        for i in range(0, grid_size, grid_width - 1):
            if completion_grid[i] == 1:
                bingo_count += 1
        if bingo_count == 4:
            bingos[2] = True
            bingos['bingo_diag'] = 3
            bingos['bingo_points'] += settings.BINGO_COMPLETE
        bingo_count = 0

    if len(all_tiles) == grid_size:
        # Check for full bingo
        if all(completion_grid):
            bingos['full_bingo'] = True
            bingos['bingo_points'] += settings.GRID_COMPLETE
    return bingos
