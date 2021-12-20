import util
import itertools
from collections import defaultdict

algorithm, image_string = util.read_file("inputs/day20.txt").strip().split("\n\n")


def parse_image(image_string):
    image = {}
    rows = image_string.split("\n")
    for y in range(0, len(rows)):
        for x in range(0, len(rows[y])):
            if rows[y][x] == "#":
                image[x, y] = 1
    return image, len(rows[0]), len(rows)


def get_adjacent(x, y):
    l = []
    for yn in range(y-1, y+2):
        for xn in range(x-1, x+2):
            l.append((xn, yn))
    return l


def get_binary_key(image, x, y, min_x, max_x, min_y, max_y, boundary):
    key = ""
    for xn, yn in get_adjacent(x, y):
        if (xn >= min_x and xn <= max_x and yn >= min_y and yn <= max_y):
            if (xn, yn) in image:
                key = key + "1"
            else:
                key = key + "0"
        else:
            key = key + boundary
    return int(key, 2)


def enhance(count):
    image, max_x, max_y = parse_image(image_string)
    for i in range(count):
        new_image = {}
        for x in range(-2 - i, max_x + 3 + i):
            for y in range(-2 - i, max_y + 3 + i):
                key = get_binary_key(image, x, y, -i, max_x + i, -i, max_y + i, "0" if i % 2 == 0 else "1")
                if algorithm[key] == "#":
                    new_image[(x, y)] = 1

        image = new_image.copy()

    return util.count_if(image.values(), lambda x: x == 1)


def part1():
    print(enhance(2))


def part2():
    print(enhance(50))
