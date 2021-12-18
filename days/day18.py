import util
from dataclasses import dataclass, field
from typing import Type
import math
from functools import reduce


@dataclass
class Number:
    value: int = None
    left: Type["Node"] = None
    right: Type["Node"] = None
    parent: Type["Node"] = field(repr=False, default=None)


def parenthetic_split(string):
    stack = []
    for i, c in enumerate(string):
        if c == '[':
            stack.append(i)
        elif c == ",":
            if len(stack) == 1:
                start = stack.pop()
                return string[start + 1: i], string[i+1:-1]
        elif c == ']' and stack:
            stack.pop()


def parse_number_util(string: str):
    left, right = parenthetic_split(string)
    left = Number(int(left)) if left.isdigit() else parse_number(left)
    right = Number(int(right)) if right.isdigit() else parse_number(right)
    return Number(left=left, right=right)


def parse_number(string: str):
    number = parse_number_util(string)
    set_parent(number)
    return number


def set_parent(number: Number, parent=None):
    number.parent = parent
    if number.left:
        set_parent(number.left, number)
    if number.right:
        set_parent(number.right, number)


def find_first_right_child(number):
    if number == None:
        return None
    if number.value != None:
        return number
    return find_first_right_child(number.right)


def find_first_left(number: Number):
    if number.parent:
        if number.parent.left is number:
            return find_first_left(number.parent)
        else:
            return find_first_right_child(number.parent.left)
    return None


def find_first_left_child(number):
    if number == None:
        return None
    if number.value != None:
        return number
    return find_first_left_child(number.left)


def find_first_right(number: Number):
    if number.parent:
        if number.parent.right is number:
            return find_first_right(number.parent)
        else:
            return find_first_left_child(number.parent.right)
    return None


def try_explode(number: Number, depth=0):
    if not number or number.value != None:
        return False

    if depth == 4:
        if first_left := find_first_left(number):
            first_left.value += number.left.value
        if first_right := find_first_right(number):
            first_right.value += number.right.value
        number.left = None
        number.right = None
        number.value = 0
        return True

    if try_explode(number.left, depth+1):
        return True
    if try_explode(number.right, depth+1):
        return True
    return False


def try_split(number: Number):
    if not number:
        return False
    if number.value != None and number.value >= 10:
        number.left = Number(math.floor(number.value / 2), parent=number)
        number.right = Number(math.ceil(number.value / 2), parent=number)
        number.value = None
        return True
    if try_split(number.left):
        return True
    if try_split(number.right):
        return True
    return False


def reduce_number(number):
    while True:
        exploded = try_explode(number)
        if exploded:
            continue
        splitted = try_split(number)
        if not exploded and not splitted:
            break
    return number


def add(a, b):
    new_number = Number(left=a, right=b)
    a.parent = new_number
    b.parent = new_number
    reduce_number(new_number)
    return new_number


numbers = util.read_lines("inputs/day18.txt", parse_number)


def magnitude(number):
    if number.value != None:
        return number.value
    return 3 * magnitude(number.left) + 2 * magnitude(number.right)


def part1():
    res = reduce(add, numbers)
    print(magnitude(res))


def part2():
    max_magnitude = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j:
                org_numbers = util.read_lines("inputs/day18.txt", parse_number)
                res = add(org_numbers[i], org_numbers[j])
                max_magnitude = max(max_magnitude, magnitude(res))
    print(max_magnitude)
