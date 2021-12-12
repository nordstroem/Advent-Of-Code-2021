import util
from collections import defaultdict


def parse(string):
    return string.split("-")


node_list = util.read_lines("inputs/day12.txt", parse)
nodes = defaultdict(list)
for fr, to in node_list:
    nodes[fr].append(to)
    nodes[to].append(fr)


def get_num_paths(fr, to, visited_small_nodes, can_visit_small_again):
    if fr == to:
        return 1
    num_paths = 0
    if fr.islower():
        visited_small_nodes.append(fr)
    for nb in nodes[fr]:
        if nb not in visited_small_nodes:
            num_paths += get_num_paths(nb, to, visited_small_nodes.copy(), can_visit_small_again)
        elif can_visit_small_again and nb != "start" and nb != "end":
            num_paths += get_num_paths(nb, to, visited_small_nodes.copy(), False)

    return num_paths


def part1():
    print(get_num_paths("start", "end", list(), False))


def part2():
    print(get_num_paths("start", "end", list(), True))
