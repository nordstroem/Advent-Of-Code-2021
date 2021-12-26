import util
import numpy as np
import heapq
import math
from collections import defaultdict
from itertools import count
from functools import lru_cache
import cProfile

converter = {"A": 0, "B": 1, "C": 2, "D": 3, ".": 4, "#": 5}


def parse(line):
    line = line.ljust(11, "#").rjust(13, "#")
    line = [converter[c] for c in util.split(line)]
    return np.array(list(map(int, line)), dtype=np.uint8)


org_grid = np.array(util.read_lines("inputs/day23.txt", parse), dtype=np.uint8)
rows, cols = org_grid.shape

rooms = {0: [(2, 3), (3, 3)], 1: [(2, 5), (3, 5)], 2: [(2, 7), (3, 7)], 3: [(2, 9), (3, 9)]}

target_grid = ["#############", "#...........#", "###A#B#C#D###", "###A#B#C#D###", "#############"]
target_grid = np.array([parse(line) for line in target_grid])
tiebreaker = count()


@lru_cache(None)
def get_adjacent(r, c):
    def inside(rt, ct): return 0 <= rt < rows and 0 <= ct < cols and org_grid[r, c] != 5

    possible = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    return [(r, c) for (r, c) in possible if inside(r, c)]


def get_invalid_spots(r0, c0, grid):
    invalid_spots = set()
    a_type = grid[r0, c0]
    for room, coord in rooms.items():
        if a_type == room:
            gc0 = grid[coord[0]]
            gc1 = grid[coord[1]]
            occupied = (gc0 != a_type and gc0 != converter["."]) or (gc1 != a_type and gc1 != converter["."])
            if occupied:
                invalid_spots.add(coord[0])
                invalid_spots.add(coord[1])
        else:
            if (r0, c0) not in coord:
                invalid_spots.add(coord[0])
                invalid_spots.add(coord[1])

    return invalid_spots


def can_walk_into(r0, c0, rt, ct, grid, invalid_spots):
    if grid[rt, ct] != 4:
        return False

    return (rt, ct) not in invalid_spots


@lru_cache(None)
def valid_stop(r0, c0, rt, ct):
    invalid_stops = [(1, 3), (1, 5), (1, 7), (1, 9)]
    was_in_hallway = True
    target_is_hallway = True
    for coord_list in rooms.values():
        for coord in coord_list:
            if coord == (r0, c0):
                was_in_hallway = False
            elif coord == (rt, ct):
                target_is_hallway = False

    return (rt, ct) not in invalid_stops and not (was_in_hallway and target_is_hallway)


# Return index, cost
def get_possible_stops(r, c, grid):
    visited = set()
    stops = set()
    s = [(r, c)]
    steps = {(r, c): 0}
    a_type = grid[r, c]
    costs = {0: 1, 1: 10, 2: 100, 3: 1000}
    cost = costs[a_type]
    while len(s) > 0:
        v = s.pop()
        if v not in visited:
            visited.add(v)
            invalid_spots = get_invalid_spots(r, c, grid)
            for rn, cn in get_adjacent(*v):
                if can_walk_into(r, c, rn, cn, grid, invalid_spots):
                    if (rn, cn) not in steps:
                        steps[rn, cn] = steps[v] + cost
                    s.append((rn, cn))
                    if valid_stop(r, c, rn, cn):
                        stops.add((rn, cn))

    return [(coord, steps[coord]) for coord in stops if coord != (r, c)]


def get_neighbor_grids(grid):
    neighbour_grids = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != converter["."] and grid[r, c] != converter["#"]:
                stops = get_possible_stops(r, c, grid)
                for coord, cost in stops:
                    new_grid = grid.copy()
                    new_grid[coord] = grid[r, c]
                    new_grid[r, c] = converter["."]
                    neighbour_grids.append((new_grid, cost))
    return neighbour_grids


def dijkstra():
    dist = defaultdict(lambda: math.inf)
    dist[org_grid.tobytes()] = 0
    q = []
    heapq.heappush(q, (0, next(tiebreaker), org_grid))
    visited = set()

    while len(q) > 0:
        score, _, u = heapq.heappop(q)
        visited.add(u.tobytes())
        if u.tobytes() == target_grid.tobytes():
            print("Done!", score)
            break

        for v, v_score in get_neighbor_grids(u):
            if v.tobytes() in visited:
                continue

            alt = dist[u.tobytes()] + v_score
            if alt < dist[v.tobytes()]:
                dist[v.tobytes()] = alt
                heapq.heappush(q, (alt, next(tiebreaker), v))

    # def part1():
    # print(valid_stop(1, 6, rn, cn))


# dijkstra()


cProfile.run("dijkstra()")


def part2():
    pass
