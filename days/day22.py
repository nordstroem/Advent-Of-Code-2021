import util
from bisect import bisect_left
import numpy as np


def parse(line):
    on, rest = line.split(" ")
    on = (on == "on")
    return on, util.extract_ints(rest)


instructions = util.read_lines("inputs/day22.txt", parse)


def count_lit(instructions):
    ons, ranges = zip(*instructions)
    x0, x1, y0, y1, z0, z1 = zip(*ranges)

    def sorted_vals(low, high):
        v = list(set(list(low) + [h+1 for h in high]))
        v.sort()
        return np.array(v)

    x, y, z = sorted_vals(x0, x1), sorted_vals(y0, y1), sorted_vals(z0, z1)
    compressed = np.zeros((len(x), len(y), len(z)), dtype=bool)
    for on, (x0, x1, y0, y1, z0, z1) in instructions:
        xmin, xmax = bisect_left(x, x0), bisect_left(x, x1+1)
        ymin, ymax = bisect_left(y, y0), bisect_left(y, y1+1)
        zmin, zmax = bisect_left(z, z0), bisect_left(z, z1+1)
        compressed[xmin:xmax, ymin:ymax, zmin:zmax] = on

    xis, yis, zis = np.nonzero(compressed[:-1, :-1, :-1])
    total = (x[xis+1] - x[xis]) * (y[yis+1] - y[yis]) * (z[zis+1] - z[zis])

    print(np.sum(total))


def part1():
    def valid_init_instruction(x0, x1, y0, y1, z0, z1):
        return x0 >= -50 and x1 <= 50 and y0 >= -50 and z1 <= 50 and z0 >= -50 and z1 <= 50

    count_lit([(on, vals) for (on, vals) in instructions if valid_init_instruction(*vals)])


def part2():
    count_lit(instructions)
