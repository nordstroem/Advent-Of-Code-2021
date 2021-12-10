import util
from collections import defaultdict

lines = util.read_lines("inputs/day10.txt")
pairs = {")": "(", "]": "[", "}": "{", ">": "<"}
pairs_inverse = {value: key for key, value in pairs.items()}


def first_corrupt_char(line):
    stack = []
    for char in line:
        if char in pairs.values():
            stack.append(char)
        elif stack[-1] == pairs[char]:
            stack.pop()
        else:
            return char
    return None


def part1():
    char_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}

    score = 0
    for line in lines:
        corrupt = first_corrupt_char(line)
        if corrupt:
            score += char_scores[corrupt]
    print(score)


def completion_string(line):
    stack = []
    for char in line:
        if char in pairs.values():
            stack.append(char)
        else:
            stack.pop()
    stack.reverse()
    stack = [pairs_inverse[c] for c in stack]
    return "".join(stack)


def part2():
    incomplete_lines = [line for line in lines if not first_corrupt_char(line)]
    char_scores = {")": 1, "]": 2, "}": 3, ">": 4}
    scores = []
    for line in incomplete_lines:
        score = 0
        for c in completion_string(line):
            score = score * 5 + char_scores[c]
        scores.append(score)

    scores.sort()
    print(scores[len(scores) // 2])
