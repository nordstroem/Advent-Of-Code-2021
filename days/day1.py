import util
import numpy as np

values = np.array(util.read_lines("inputs/day1.txt", int))


def part1():
    d = np.diff(values)
    print(np.count_nonzero(d > 0))


def part2():
    v = [np.sum(values[i:i + 3]) for i in range(len(values) - 2)]
    d = np.diff(v)
    print(np.count_nonzero(d > 0))
