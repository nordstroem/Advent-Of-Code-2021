import util
from collections import defaultdict
import numpy as np


def parse_board(string):
    rows = string.strip().split("\n")
    board = [[int(e) for e in row.split()] for row in rows]
    return np.array(board)


all_lines = util.read_file("inputs/day4.txt")
groups = all_lines.split("\n\n")
drawn_numbers = [int(v) for v in groups[0].split(",")]
boards = [parse_board(board) for board in groups[1:]]


def check_win(board, drawn_numbers):
    for row in board:
        if all([e in drawn_numbers for e in row]):
            return True
    for col in board.T:
        if all([e in drawn_numbers for e in col]):
            return True
    return False


def find_winner(boards, drawn_numbers):
    for i in range(1, len(drawn_numbers)):
        for board_nr, board in enumerate(boards):
            if check_win(board, drawn_numbers[:i]):
                return board_nr, i
    return (-1, -1)


def calculate_score(board, drawn_numbers):
    res = 0
    for e in np.nditer(board):
        if (e not in drawn_numbers):
            res += e
    return res * drawn_numbers[-1]


def part1():
    board_nr, last_drawn_index = find_winner(boards, drawn_numbers)
    print(calculate_score(boards[board_nr], drawn_numbers[:last_drawn_index]))


def part2():
    while True:
        board_nr, last_drawn_index = find_winner(boards, drawn_numbers)
        if (len(boards) == 1):
            print(calculate_score(boards[board_nr], drawn_numbers[:last_drawn_index]))
            break
        boards.pop(board_nr)
