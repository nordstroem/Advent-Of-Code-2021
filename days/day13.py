import util
import numpy as np

def parse(string):
    return string.split("-")

file = util.read_file("inputs/day13.txt")
coords, instructions = file.split("\n\n")
instructions = instructions.strip().split("\n")
coords = np.array([np.array((int(y), int(x))) for x, y in map(lambda x: x.split(","), coords.split("\n"))])
rows, cols = np.max(coords, axis=0) + 1
original_grid = np.zeros((rows, cols), dtype=np.uint8)
original_grid[coords[:,0], coords[:, 1]] = 1

def fold(grid, axis, index):
    if axis == "x":
        other = np.flip(grid[:,index+1:], axis=1)
        grid = grid[:,:index] | other
    else:
        other = np.flip(grid[index+1:,:], axis=0)
        grid = grid[:index,:] | other
    return grid

def part1():
    (axis, index) = instructions[0][11:].split("=")
    grid = fold(original_grid, axis, int(index))
    print(np.count_nonzero(grid))

def part2():
    grid = original_grid
    for instruction in instructions:
        (axis, index) = instruction[11:].split("=")
        grid = fold(grid, axis, int(index))

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 1:
                print("#", end="")
            else:
                print(" ", end="")
        print("")