from .models import TileInteraction  # noqa
import math


def check_bingo(tile):
    all_tiles = TileInteraction.objects.filter(user=tile.user, grid=tile.grid)
    grid_size = 16
    grid_width = int(math.sqrt(grid_size))
    completion_grid = grid_size*[0]
    for t in all_tiles:
        completion_grid[t.position] = 1 if t.completed else 0
    tile_row = tile.position // grid_width
    tile_col = tile.position % grid_width
    bingos = 4 * [False]

    bingo_count = 0
    for i in range(tile_row*grid_width, tile_row*grid_width+grid_width):
        if completion_grid[i] == 1:
            bingo_count += 1
    if bingo_count == 4:
        bingos[0] = True
    bingo_count = 0

    for i in range(tile_col, grid_size, grid_width):
        if completion_grid[i] == 1:
            bingo_count += 1
    if bingo_count == 4:
        bingos[1] = True
    bingo_count = 0

    if tile_row == tile_col:
        for i in range(0, grid_size, grid_width+1):
            if completion_grid[i] == 1:
                bingo_count += 1
        if bingo_count == 4:
            bingos[2] = True
        bingo_count = 0
    elif tile_row + tile_col == grid_width - 1:
        for i in range(0, grid_size, grid_width - 1):
            if completion_grid[i] == 1:
                bingo_count += 1
        if bingo_count == 4:
            bingos[2] = True
        bingo_count = 0

    if len(all_tiles) == grid_size:
        # Check for full bingo
        if all(completion_grid):
            bingos[3] = True

    return bingos
