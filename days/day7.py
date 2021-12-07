import util
from collections import defaultdict


values = list(map(int, util.read_lines("inputs/day7.txt")[0].split(",")))

def fuel_score_1(position):
    return sum([abs(value - position) for value in values])


def fuel_score_2(position):
    arithmetic_sum = lambda n : n * (n + 1) // 2
    return sum([arithmetic_sum(abs(value - position)) for value in values])


def part1():
    print(min([fuel_score_1(i) for i in range(max(values)+1)]))


def part2():
    print(min([fuel_score_2(i) for i in range(max(values)+1)]))