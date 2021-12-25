import util
import numpy as np


grid = np.array(util.read_lines("inputs/day25.txt", lambda s: util.split(s)))
rows, cols = grid.shape


def iterate(grid, horizontal):
    moved = False
    original_grid = grid.copy()
    char = ">" if horizontal else "v"
    for r, c in np.ndindex(grid.shape):
        next_pos = (r, (c + 1) % cols) if horizontal else ((r + 1) % rows, c)
        if original_grid[r, c] == char and original_grid[next_pos] == ".":
            grid[next_pos] = char
            grid[r, c] = "."
            moved = True
    return moved


def part1():
    i = 1
    while True:
        moved_h = iterate(grid, True)
        moved_v = iterate(grid, False)
        if not (moved_h or moved_v):
            print(i)
            break
        i += 1
