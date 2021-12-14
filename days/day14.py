import util
import itertools
from collections import Counter, defaultdict

template, rules = util.read_file("inputs/day14.txt").strip().split("\n\n")
rules = {key:value for key, value in [rule.split(" -> ") for rule in rules.split("\n")]}

def apply(old):
    new = []
    for i in range(len(old)-1):
        pair = "".join([old[i], old[i+1]])
        new.append(rules[pair])

    res = []
    while len(old) > 0:
        res.append(old.pop(0))
        if len(new) > 0:
            res.append(new.pop(0))
    return res

def part1():
    l = util.split(template)
    for i in range(10):
        l = apply(l)
    
    occ = Counter(l).most_common()
    print(occ[0][1] - occ[-1][1])

def apply2(pairs):
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
    
    counts["S"] -= 1
    counts["F"] -= 1
    counts = {char:count//2 for (char, count) in counts.items()}
    counts["S"] += 1
    counts["F"] += 1
    counts = list(counts.items())
    counts.sort(key=lambda a: a[1])
    counts.reverse()
    return counts

def part2():
    pairs = defaultdict(int)
    old = util.split(template)
    for i in range(len(util.split(template))-1):
        pair = "".join([old[i], old[i+1]])
        pairs[pair] += 1

    for i in range(40):
        pairs = apply2(pairs)
    occ = count_element_wise(pairs)
    print(occ[0][1] - occ[-1][1])