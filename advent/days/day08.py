from functools import reduce
from operator import mul
from typing import Iterable, Iterator, TextIO

from advent.matrix import Coord, Matrix


def cardinal_trees(c: Coord, patch: Matrix[int]) -> Iterator[Iterable[int]]:
    row, col = c

    # Left, Right, Top, Bottom
    yield reversed([patch[row, cc] for cc in range(0, col)])
    yield [patch[row, cc] for cc in range(col + 1, patch.width)]
    yield reversed([patch[rr, col] for rr in range(0, row)])
    yield [patch[rr, col] for rr in range(row + 1, patch.height)]


def is_visible(c: Coord, patch: Matrix[int]) -> bool:
    """
    A tree is visible if for any directions (top left bottom right) there is no other equal or taller tree.
    """

    row, col = c
    tree = patch[c]

    # Special case: on the edge
    if col == 0 or col == patch.width - 1 or row == 0 or row == patch.height - 1:
        return True

    # If all the trees are smaller than `tree` in any of the directions, then the tree is visible
    return any(all(t < tree for t in tree_direction) for tree_direction in cardinal_trees(c, patch))


def scenic_score_direction(tree: int, other_trees: Iterable[int]) -> int:
    score = 0
    for other in other_trees:
        score += 1
        if other >= tree:
            return score
    return score


def scenic_score(c: Coord, patch: Matrix[int]) -> int:
    tree = patch[c]
    direction_scores = [scenic_score_direction(tree, tree_direction) for tree_direction in cardinal_trees(c, patch)]

    return reduce(mul, direction_scores, 1)


def first(input: TextIO) -> int:
    patch = Matrix.from_string(input.read(), fn=int)
    return sum(is_visible(c, patch) for c in patch.all_coords())


def second(input: TextIO) -> int:
    patch = Matrix.from_string(input.read(), fn=int)
    return max(scenic_score(c, patch) for c in patch.all_coords())
