import util
import numpy as np
from functools import reduce
import operator

def parse(string):
    return list(map(int, util.split(string)))


values = np.array(util.read_lines("inputs/day9.txt", parse))
rows, cols = values.shape

def get_adjacent(r, c):
    adj = []
    inside = lambda r, c: r >= 0 and r < rows and c >= 0 and c < cols
    possible = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
    for r, c in possible:
        if inside(r, c):
            adj.append((r,c))
    return adj

def get_low_points():
    low_points = []
    for r in range(0, rows):
        for c in range(0, cols):
            if all(values[r, c] < [values[rn, cn] for rn, cn in get_adjacent(r, c)]):
                low_points.append((r, c))

    return low_points

def part1():
    risk_sum = 0
    for r, c in get_low_points():
        risk_sum += 1 + values[r, c]
    print(risk_sum)

def get_flow_path(r, c):
    flow_path = {(r, c)}
    for rn, cn in get_adjacent(r, c):
        if values[rn, cn] > values[r, c] and values[rn, cn] != 9:
            flow_path = flow_path.union(get_flow_path(rn, cn))
    return flow_path

def part2():
    basin_sizes = [len(get_flow_path(r, c)) for r, c in get_low_points()]
    basin_sizes.sort()
    basin_sizes.reverse()
    print(reduce(operator.mul, basin_sizes[0:3], 1))
