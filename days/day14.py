import util
from collections import defaultdict

template, rules = util.read_file("inputs/day14.txt").strip().split("\n\n")
rules = {key:value for key, value in [rule.split(" -> ") for rule in rules.split("\n")]}


def get_pairs(template):
    pairs = defaultdict(int)
    template = util.split(template)
    for i in range(len(template)-1):
        pair = "".join([template[i], template[i+1]])
        pairs[pair] += 1
    return pairs


def apply(pairs):
    new_pairs = defaultdict(int)
    for pair, count in pairs.items():
        p0 = pair[0]+rules[pair]
        p1 = rules[pair]+pair[1]
        new_pairs[p0] += count
        new_pairs[p1] += count
    return new_pairs


def count_element_wise(pairs):
    counts = defaultdict(int)
    for (p0, p1), count in pairs.items():
        counts[p0] += count
        counts[p1] += count
    
    counts = {char:round(count/2) for (char, count) in counts.items()}
    counts = list(counts.items())
    counts.sort(key=lambda a: a[1])
    counts.reverse()
    return counts


def iterate(count):
    pairs = get_pairs(template)
    for i in range(count):
        pairs = apply(pairs)
    occ = count_element_wise(pairs)
    return occ[0][1] - occ[-1][1]


def part1():
    print(iterate(10))


def part2():
    print(iterate(40))