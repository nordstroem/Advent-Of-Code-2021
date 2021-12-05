import util
import numpy as np
from collections import defaultdict


def parse(string):
    vals = string.split()[::2]
    vals = [v.split(",") for v in vals]
    return (int(vals[0][0]), int(vals[0][1])), (int(vals[1][0]), int(vals[1][1]))


values = util.read_lines("inputs/day5.txt", parse)


def count_intersections(count_diagonals):
    intersections = defaultdict(int)
    for f, t in values:
        dx = np.sign(t[0] - f[0])
        dy = np.sign(t[1] - f[1])
        p = f
        if (count_diagonals or (dx == 0 or dy == 0)):
            while(p != (t[0] + dx, t[1] + dy)):
                intersections[p] += 1
                p = (p[0] + dx, p[1] + dy)

    return util.count_if(intersections.values(), lambda x: x >= 2)


def part1():
    print(count_intersections(False))


def part2():
    print(count_intersections(True))
