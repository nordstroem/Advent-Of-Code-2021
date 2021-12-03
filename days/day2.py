import util


def split_line(line):
    (command, value) = line.split()
    return command, int(value)


values = util.read_lines("inputs/day2.txt", split_line)


def part1():
    x = 0
    y = 0
    for (command, value) in values:
        if command == "forward":
            x += value
        elif command == "down":
            y -= value
        else:
            y += value

    print(x * y)


def part2():
    aim = 0
    x = 0
    y = 0
    for (command, value) in values:
        if command == "forward":
            x += value
            y += aim * value
        elif command == "down":
            aim += value
        else:
            aim -= value

    print(x * y)
