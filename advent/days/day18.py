from collections import Counter, deque
from typing import List, TextIO, Tuple

Pos = Tuple[int, int, int]


def get_nc(p: Pos) -> List[Pos]:
    nc_deltas = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
    return [(p[0] + dx, p[1] + dy, p[2] + dz) for dx, dy, dz in nc_deltas]


def first(input: TextIO) -> int:
    coords = [tuple(map(int, l.split(','))) for l in input.read().splitlines()]
    return sum(sum(map(lambda p: 1 if p not in coords else 0, get_nc(c))) for c in coords)


def second(input: TextIO) -> int:
    lava_cells = set([tuple(map(int, l.split(','))) for l in input.read().splitlines()])
    # There will be outside_cells dups because we're not counting surfaces
    outside_cells = [p for c in lava_cells for p in get_nc(c) if p not in lava_cells]
    counts = Counter(outside_cells)

    # Pick a starting cell, for instance the one with the lowest x
    surface_area = 0
    seen = set()
    candidates = deque([sorted(outside_cells, key=lambda x: x[0])[0]])

    # The strategy is to map out all the cells +outside+ of the lava drop, by starting with a known cell outside, we
    # should be able to reach all the other cells surrounding the lava drop because there is a single lava drop. All the
    # "outside_cells" that we haven't reached are actually air bubbles
    while candidates:
        current = candidates.popleft()
        if current in seen:
            # It's possible we have dup candidates
            continue

        if current not in counts:
            # This candidate does not have any surface
            continue

        seen.add(current)
        surface_area += counts[current]

        # Add the neighbors to keep exploring, we're adding 2 levels deep to work around corners
        for n in get_nc(current):
            if (n not in seen) and (n not in lava_cells):
                candidates.append(n)
                for nn in get_nc(n):
                    if (n not in seen) and (n not in lava_cells):
                        candidates.append(nn)

    return surface_area
