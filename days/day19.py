import util
import numpy as np
import itertools
from scipy.spatial.transform import Rotation
from scipy import linalg
from collections import defaultdict


def parse():
    blocks = util.read_file("inputs/day19.txt").strip().split("\n\n")
    scs = []
    for block in blocks:
        lines = block.split("\n")[1:]
        scanner = [util.extract_ints(line) for line in lines]
        scs.append(np.array(scanner, dtype=int))
    return scs


rotations = Rotation.create_group("O").as_matrix().astype(int)
scanners = parse()


def relative_transform(a: np.ndarray, b: np.ndarray):
    offsets = defaultdict(list)

    for i0, i1 in itertools.combinations(range(len(a)), 2):
        offset = a[i0] - a[i1]
        offsets[tuple(offset)].append((i0, i1))
        offsets[tuple(-offset)].append((i1, i0))

    possible_offsets = defaultdict(set)
    for i0, i1 in itertools.combinations(range(len(b)), 2):
        for ri, r in enumerate(rotations):
            bp = b @ r.T
            offset = bp[i0] - bp[i1]
            if tuple(offset) in offsets:
                for (ai0, ai1) in offsets[tuple(offset)]:
                    offset0 = tuple(a[ai0] - bp[i0])
                    offset1 = tuple(a[ai1] - bp[i1])
                    if offset0 == offset1:
                        possible_offsets[ri, offset0].add(i0)
                        possible_offsets[ri, offset1].add(i1)

    for (ri, offset), indices in possible_offsets.items():
        if len(indices) >= 12:
            return rotations[ri], np.array(offset)

    return None


def path(fr, to, maps, visited):
    visited.add((fr, to))
    if fr == to:
        return []
    if (fr, to) in maps:
        return [(fr, to)]

    for (i0, i1) in maps:
        if i0 == fr and (i1, to) not in visited:
            if tp := path(i1, to, maps, visited):
                return [(fr, i1)] + tp

    return []


def get_transforms(scanners):
    def inverse(rotation: np.ndarray, offset: np.ndarray):
        inv_rotation = linalg.inv(rotation)
        return inv_rotation, -offset @ inv_rotation.T

    transforms = {}
    for i0, i1 in itertools.combinations(range(len(scanners)), 2):
        if r_offset := relative_transform(scanners[i0], scanners[i1]):
            transforms[i1, i0] = r_offset
            r, offset = r_offset
            transforms[i0, i1] = inverse(r, offset)

    return transforms


def part1():
    transforms = get_transforms(scanners)
    normalized_scanners = [scanners[0]]
    for i, scanner in enumerate(scanners[1:]):
        for t in path(i + 1, 0, transforms.keys(), set()):
            r, offset = transforms[t]
            scanner = offset + scanner @ r.T
        normalized_scanners.append(scanner)

    coordinates = set()
    for scanner in normalized_scanners:
        for coord in scanner:
            coordinates.add(tuple(coord))

    print(len(coordinates))


def part2():
    transforms = get_transforms(scanners)
    offsets = []
    for i in range(0, len(scanners)):
        offset = np.array([0, 0, 0], dtype=int)
        for t in path(i, 0, transforms.keys(), set()):
            r, t_offset = transforms[t]
            offset = t_offset + offset @ r.T
        offsets.append(offset)

    max_distance = -1
    for i0, i1 in itertools.combinations(range(len(offsets)), 2):
        max_distance = max(max_distance, linalg.norm(offsets[i0] - offsets[i1], ord=1))
    print(max_distance)
