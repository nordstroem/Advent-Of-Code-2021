import util
from collections import defaultdict


def parse(string):
    patterns, output = string.split("|")
    return patterns.split(), output.split()


values = util.read_lines("inputs/day8.txt", parse)


def part1():
    res = 0
    for pattern, output in values:
        res += util.count_if(output, lambda x: (len(x) >= 2 and len(x) <= 4) or len(x) == 7)
    print(res)


def get_cipher(patterns):
    cipher = {}

    char_count = defaultdict(int)
    for pattern in patterns:
        for char in pattern:
            char_count[char] += 1

    cipher["e"] = next(char for char, count in char_count.items() if count == 4)
    cipher["b"] = next(char for char, count in char_count.items() if count == 6)
    cipher["f"] = next(char for char, count in char_count.items() if count == 9)

    three_chars = set(next(pattern for pattern in patterns if len(pattern) == 3))
    two_chars = set(next(pattern for pattern in patterns if len(pattern) == 2))
    cipher["a"] = (three_chars - two_chars).pop()
    cipher["c"] = next(char for char, count in char_count.items() if count == 8 and char not in cipher.values())

    four_chars = next(pattern for pattern in patterns if len(pattern) == 4)
    cipher["d"] = next(char for char, count in char_count.items() if count == 7 and char in four_chars)
    cipher["g"] = next(char for char, count in char_count.items() if count == 7 and char not in cipher.values())

    cipher = {value: key for key, value in cipher.items()}

    return cipher


def part2():
    patterns, output = values[0]

    digit_map = {0: "abcefg", 1: "cf", 2: "acdeg", 3: "acdfg", 4: "bcdf", 5: "abdfg", 6: "abdefg", 7: "acf", 8: "abcdefg", 9: "abcdfg"}
    digit_map = {key: set(value) for key, value in digit_map.items()}

    res = 0
    for patterns, outputs in values:
        cipher = get_cipher(patterns)
        part_res = ""
        for output in outputs:
            deciphred = set([cipher[char] for char in output])
            digit = next(digit for digit, chars in digit_map.items() if chars == deciphred)
            part_res += str(digit)
        res += int(part_res)
    print(res)
