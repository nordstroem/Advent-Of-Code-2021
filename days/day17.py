import util
import numpy as np
from dataclasses import dataclass, field


@dataclass
class Point:
    x: float
    y: float


target_x = (70, 125)
target_y = (-159, -121)


def inside_target(p):
    return p.x >= target_x[0] and p.x <= target_x[1] and p.y >= target_y[0] and p.y <= target_y[1]


def can_reach_target(vel):
    pos = Point(0, 0)
    highest_point = 0
    while pos.x <= target_x[1] and pos.y >= target_y[0]:
        highest_point = max(highest_point, pos.y)
        if inside_target(pos):
            return True, highest_point
        pos.x += vel.x
        pos.y += vel.y
        vel.x += -np.sign(vel.x)
        vel.y -= 1

    return False, highest_point


def part1():
    max_y = 0
    for vx in range(target_x[1]+1):
        for vy in range(-200, 200):
            reached, top = can_reach_target(Point(vx, vy))
            if reached:
                max_y = max(max_y, top)
    print(max_y)


def part2():
    count = 0
    for vx in range(target_x[1]+1):
        for vy in range(-200, 200):
            reached, top = can_reach_target(Point(vx, vy))
            if reached:
                count += 1
    print(count)
