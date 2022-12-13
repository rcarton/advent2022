from heapq import heappop, heappush
from typing import List, TextIO

from advent.matrix import Coord, Matrix

HeightMap = Matrix[str]


def find_starting_pos(m: HeightMap) -> Coord:
    for c in m.all_coords():
        if m[c] == 'S':
            return c
    raise Exception('Starting position not found')


def find_all_starting_pos(m: HeightMap) -> List[Coord]:
    result = []
    for c in m.all_coords():
        if m[c] == 'S' or m[c] == 'a':
            result.append(c)
    return result


def elevation(v: str) -> int:
    return ord(v if v != 'S' else 'a')


def find_path(m: HeightMap, starting_pos: List[Coord]) -> List[Coord]:
    visited = set(starting_pos)
    to_visit = []
    for S in starting_pos:
        heappush(to_visit, (0, [S]))

    while to_visit:
        cost, prev = heappop(to_visit)
        current: Coord = prev[-1]

        for neighbor in m.neighbor_coords(current):
            if elevation(m[neighbor]) - elevation(m[current]) <= 1 and neighbor not in visited:
                if m[neighbor] == 'z':
                    return prev + [neighbor]

                visited.add(neighbor)
                # Cost is 1 because we only consider the number of moves
                heappush(to_visit, (cost + 1, prev + [neighbor]))

    raise Exception('No path found')


def first(input: TextIO) -> int:
    m = HeightMap.from_string(input.read())
    return len(find_path(m, [find_starting_pos(m)]))


def second(input: TextIO) -> int:
    m = HeightMap.from_string(input.read())
    return len(find_path(m, find_all_starting_pos(m)))
