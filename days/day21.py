import util
import itertools
from functools import lru_cache


def part1():
    def new_pos(old_pos, iteration): return (old_pos + 9*iteration + 6 - 1) % 10 + 1
    p1, p2 = 10, 7
    die_iter = 0
    p1_score = 0
    p2_score = 0
    while True:
        p1 = new_pos(p1, die_iter)
        die_iter += 1
        p1_score += p1
        if p1_score >= 1000:
            break
        p2 = new_pos(p2, die_iter)
        die_iter += 1
        p2_score += p2
        if p2_score >= 1000:
            break

    print(min(p1_score, p2_score) * die_iter * 3)


@lru_cache(maxsize=None)
def num_wins(pos, score, opponent_pos, opponent_score, die_turn):
    if opponent_score >= 21:
        return 0
    if score >= 21:
        return 1
    wins = 0
    if die_turn <= 2:
        wins = 0
        for i in range(1, 4):
            new_pos = (pos + i - 1) % 10 + 1
            new_score = score + new_pos if die_turn == 2 else score
            wins += num_wins(new_pos, new_score, opponent_pos, opponent_score, (die_turn+1) % 6)
    else:
        wins = 0
        for i in range(1, 4):
            new_pos = (opponent_pos + i - 1) % 10 + 1
            new_score = opponent_score + new_pos if die_turn == 5 else opponent_score
            wins += num_wins(pos, score, new_pos, new_score, (die_turn+1) % 6)
    return wins


def part2():
    p1_wins = num_wins(10, 0, 7, 0, 0)
    p2_wins = num_wins(7, 0, 10, 0, 3)
    print(max(p1_wins, p2_wins))
