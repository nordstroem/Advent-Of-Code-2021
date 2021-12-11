import util
from collections import defaultdict
import numpy as np
import itertools


def parse(string):
    return list(map(int, util.split(string)))


original_grid = np.array(util.read_lines("inputs/day11.txt", parse))
rows, cols = original_grid.shape


def get_adjacent(r, c):
    adj = []
    for rn, cn in itertools.product(range(max(r-1, 0), min(r+2, rows)), range(max(c-1, 0), min(c+2, cols))):
        if (rn, cn) != (r, c):
            adj.append((rn, cn))
    return adj


def flash(grid, r, c, flashed_indices):
    if (r, c) in flashed_indices:
        return
    flashed_indices.add((r, c))
    for (rn, cn) in get_adjacent(r, c):
        grid[rn, cn] += 1
        if grid[rn, cn] > 9:
            flash(grid, rn, cn, flashed_indices)


def iterate(grid):
    flashed_indices = set()
    for r, c in itertools.product(range(rows), range(cols)):
        grid[r, c] += 1
        if (grid[r, c] > 9):
            flash(grid, r, c, flashed_indices)

    for r, c in flashed_indices:
        grid[r, c] = 0

    return len(flashed_indices)


def part1():
    grid = original_grid
    total_flashes = 0
    for i in range(100):
        total_flashes += iterate(grid)
    print(total_flashes)


def part2():
    grid = original_grid
    step = 1
    while True:
        if iterate(grid) == grid.size:
            print(step)
            break
        step += 1
