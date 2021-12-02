import math
from functools import reduce


def read_lines(path, fun=lambda x: x):
    with open(path, 'r') as inp:
        lines = inp.readlines()
        return [fun(l.strip()) for l in lines]


def read_file(path):
    with open(path, 'r') as inp:
        return inp.read()


def count_if(container, predicate):
    count = 0
    for element in container:
        if predicate(element):
            count = count + 1
    return count


def split(line):
    return [char for char in line]


def lcm(*args):
    return reduce(lambda a, b: a * b // math.gcd(a, b), args)


def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0
