import util
from collections import defaultdict


values = list(map(int, util.read_lines("inputs/day6.txt")[0].split(",")))
initial = defaultdict(int)
for value in values:
    initial[value] += 1
    
def iterate(current, count):
    for _ in range(count):
        next = defaultdict(int)
        for key in current.keys():
            if key != 0:
                next[key-1] = current[key]

        next[8] = current[0]
        next[6] += current[0]
        current = next
    return current

def part1():
    print(sum(iterate(initial, 80).values()))

def part2():
    print(sum(iterate(initial, 256).values()))
