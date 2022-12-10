from typing import List, TextIO, Tuple

from advent.matrix import Coord

# Move deltas (<row delta>, <column delta>)
MOVES = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}


def get_new_tail(head: Coord, tail: Coord) -> Coord:
    hr, hc = head
    tr, tc = tail
    dr, dc = hr - tr, hc - tc

    if abs(dr) <= 1 and abs(dc) <= 1:
        # No need to move, head and tail are still touching
        return tail

    tr = tr + int(bool(dr)) * (-1 if dr < 0 else 1)
    tc = tc + int(bool(dc)) * (-1 if dc < 0 else 1)

    return tr, tc


def update_rope(move: Tuple[int, int], rope: List[Coord]) -> None:
    d_row, d_col = move

    # New head
    head = rope[0]
    head = (head[0] + d_row, head[1] + d_col)
    rope[0] = head

    # Now update every segment
    for i in range(1, len(rope)):
        new_tail = get_new_tail(head, rope[i])
        rope[i] = new_tail
        head = new_tail


def get_all_tail_positions(rope: List[Coord], moves_s: List[str]) -> int:
    visited = {rope[-1]}

    for move in moves_s:
        dir, count = move.split(' ')
        for _ in range(int(count)):
            update_rope(MOVES[dir], rope)
            visited.add(rope[-1])

    return len(visited)


def first(input: TextIO) -> int:
    return get_all_tail_positions([(0, 0)] * 2, input.read().splitlines())


def second(input: TextIO) -> int:
    return get_all_tail_positions([(0, 0)] * 10, input.read().splitlines())
