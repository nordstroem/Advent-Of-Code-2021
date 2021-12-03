import util
from collections import defaultdict

all_lines = util.read_lines("inputs/day3.txt")
bits = len(all_lines[0])

def get_most_common_bits(lines):
    N = len(lines)
    one_count = defaultdict(int)
    for line in lines:
        for i in range(bits):
            if line[i] == "1":
                one_count[i] += 1

    def rule(val):
        if val == N/2:
            return 1
        else:
            return 1 if val > N/2 else 0

    most_common_bits = {i: rule(val) for (i, val) in one_count.items()}
    return most_common_bits

def part1():
    most_common_bits = get_most_common_bits(all_lines)
    gamma_rate = ""
    epsilon_rate = ""
    for i in range(bits):
        gamma_rate += str(most_common_bits[i])
        epsilon_rate += str(1-most_common_bits[i])

    print(int(gamma_rate, 2) * int(epsilon_rate, 2))


def get_rating(lines, invert):
    bit = 0
    while(len(lines) > 1):
        mcb = get_most_common_bits(lines)
        lines = [l for l in lines if l[bit] == str(1 - mcb[bit] if invert else mcb[bit])]
        bit += 1
    return(int(lines[0], 2))


def part2():
    o = get_rating(all_lines, False)
    c = get_rating(all_lines, True)
    print(o * c)
