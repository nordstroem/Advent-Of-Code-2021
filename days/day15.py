import util
from collections import defaultdict
import numpy as np
import networkx as nx
import itertools

base_grid = np.array(util.read_lines("inputs/day15.txt", lambda x: list(map(int, util.split(x)))), dtype=np.uint8)
b_rows, b_cols = base_grid.shape


def adjacent(r, c, rows, cols):
    def inside(r, c): return r >= 0 and r < rows and c >= 0 and c < cols
    return [(r, c) for r, c in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)] if inside(r, c)]


def smallest_risk(grid):
    G = nx.DiGraph()
    g_rows, g_cols = grid.shape
    for c in itertools.product(range(g_rows), range(g_cols)):
        for nb in adjacent(*c, g_rows, g_cols):
            G.add_edge(c, nb, weight=grid[nb])

    path = nx.shortest_path(G, (0, 0), (g_rows-1, g_cols-1), weight='weight')
    return nx.path_weight(G, path, weight="weight")


def part1():
    print(smallest_risk(base_grid))


def new_risk(old, tile_r, tile_c):
    return (old - 1 + tile_r + tile_c) % 9 + 1


def part2():
    new_rows = 5 * b_rows
    new_cols = 5 * b_cols
    new_grid = np.zeros((new_rows, new_cols), dtype=np.uint8)
    for r, c in itertools.product(range(new_rows), range(new_cols)):
        base_risk = base_grid[r % b_rows, c % b_cols]
        new_grid[r, c] = new_risk(base_risk, r // b_rows, c // b_cols)

    print(smallest_risk(new_grid))
