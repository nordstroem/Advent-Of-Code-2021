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

room_range = range(2, 4)
costs = {0: 1, 1: 10, 2: 100, 3: 1000}

target_grid = ["#############", "#...........#", "###A#B#C#D###", "###A#B#C#D###", "#############"]
target_grid = np.array([parse(line) for line in target_grid])
tiebreaker = count()


def get_rooms():
    rooms = {}
    c_cols = {0: 3, 1: 5, 2: 7, 3: 9}
    for room, col in c_cols.items():
        rooms[room] = [(r, col) for r in room_range]
    return rooms


rooms = get_rooms()


@lru_cache()
def get_corridor():
    coordinates = []
    for r in range(rows):
        for c in range(cols):
            if org_grid[r, c] != converter["#"]:
                coordinates.append((r, c))
    return coordinates


@lru_cache(None)
def get_adjacent(r, c):
    def inside(rt, ct): return 0 <= rt < rows and 0 <= ct < cols and org_grid[r, c] != 5

    possible = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    return [(r, c) for (r, c) in possible if (inside(r, c) and (r, c) in get_corridor())]


def get_invalid_spots(r0, c0, grid):
    invalid_spots = set()
    a_type = grid[r0, c0]
    for room, coord in get_rooms().items():
        if a_type == room:
            occupied = False
            for c in coord:
                occupied = occupied or grid[c] != a_type and grid[c] != converter["."]
            if occupied:
                for c in coord:
                    invalid_spots.add(c)
        else:
            if (r0, c0) not in coord:
                for c in coord:
                    invalid_spots.add(c)

    return invalid_spots


@lru_cache(None)
def valid_stop(r0, c0, rt, ct):
    invalid_stops = [(1, 3), (1, 5), (1, 7), (1, 9)]
    was_in_hallway = True
    target_is_hallway = True
    for coord_list in get_rooms().values():
        for coord in coord_list:
            if coord == (r0, c0):
                was_in_hallway = False
            elif coord == (rt, ct):
                target_is_hallway = False

    return (rt, ct) not in invalid_stops and not (was_in_hallway and target_is_hallway)


# Return index, cost
# This is really slow. plz fix.
def get_possible_stops(r, c, grid):
    visited = set()
    stops = set()
    s = [(r, c)]
    steps = {(r, c): 0}
    a_type = grid[r, c]
    cost = costs[a_type]
    invalid_spots = get_invalid_spots(r, c, grid)

    while len(s) > 0:
        v = s.pop()
        if v not in visited:
            visited.add(v)
            for rn, cn in get_adjacent(*v):
                if grid[rn, cn] == 4 and (rn, cn) not in invalid_spots:
                    if (rn, cn) not in steps:
                        steps[rn, cn] = steps[v] + cost
                    s.append((rn, cn))
                    if valid_stop(r, c, rn, cn):
                        stops.add((rn, cn))

    return [(coord, steps[coord]) for coord in stops if coord != (r, c)]


def get_neighbor_grids(grid):
    neighbour_grids = []
    for r, c in get_corridor():
        if grid[r, c] != converter["."]:
            stops = get_possible_stops(r, c, grid)
            for coord, cost in stops:
                new_grid = grid.copy()
                new_grid[coord] = grid[r, c]
                new_grid[r, c] = converter["."]
                neighbour_grids.append((new_grid, cost))
    return neighbour_grids


def heuristic(grid):
    h = 0
    base_c = {0: 3, 1: 5, 2: 7, 3: 9}
    for r, c in get_corridor():
        a_type = grid[r, c]
        if a_type != converter["."]:
            h += costs[a_type] * abs(c - base_c[a_type])
    return h


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
            print("Done!", dist[u.tobytes()])
            break

        for v, v_score in get_neighbor_grids(u):
            if v.tobytes() in visited:
                continue

            alt = dist[u.tobytes()] + v_score
            if alt < dist[v.tobytes()]:
                dist[v.tobytes()] = alt
                h = heuristic(v)
                heapq.heappush(q, (alt + h, next(tiebreaker), v))

    # def part1():
    # print(valid_stop(1, 6, rn, cn))


# dijkstra()


cProfile.run("dijkstra()")


def part2():
    pass
