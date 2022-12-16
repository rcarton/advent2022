import re
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import List, TextIO, Tuple

from advent.matrix import Coord


@dataclass
class Sensor:
    pos: Coord
    beacon: Coord


def dist(c1: Coord, c2: Coord) -> int:
    """Manhattan distance"""
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


Segment = Tuple[int, int]


def row_intersect(row: int, sensor: Sensor) -> Segment | None:
    """Return the intersection, start and end are inclusive."""
    radius = dist(sensor.pos, sensor.beacon)

    sr, sc = sensor.pos

    # Escape hatch
    if not (sr - radius <= row <= sr + radius):
        return None

    # Figure out the radius at the row
    row_radius = 1 + 2 * (radius - abs(sr - row))

    return (sc - row_radius // 2, sc + row_radius // 2)


def parse(input: str) -> List[Sensor]:
    result = []
    for line in input.rstrip().splitlines():
        sc, sr, bc, br = map(int, re.findall(r'-?\d+', line))
        result.append(Sensor((sr, sc), (br, bc)))
    return result


def merge_segments(segments: List[Segment]) -> List[Segment]:
    # Sort the segments by starting value
    segments = deque(sorted(segments, key=lambda segment: segment[0]))

    # Try to merge all the segments
    merged = []

    while segments:
        start, end = segments.popleft()
        if not len(merged):
            merged.append((start, end))
            continue

        last_start, last_end = merged[-1]

        # Update the end if they overlap
        if last_end >= start:
            merged[-1] = (last_start, max(end, last_end))
            continue

        # No overlap, we add the new segment
        merged.append((start, end))

    return merged


def count_impossible_positions_in_row(sensors: List[Sensor], row: int) -> int:
    # Find all the intersects, they can overlap
    segments = [intersect for s in sensors if (intersect := row_intersect(row, s)) is not None]

    # Sort the segments by starting value
    merged_segments = merge_segments(segments)

    sensors_c = [s.pos for s in sensors]
    beacons = [s.beacon for s in sensors]

    # Get column for all sensors and beacons on the row
    busy_columns = set(c for r, c in sensors_c + beacons if r == row)

    # Get the count
    count = sum(end - start + 1 for start, end in merged_segments)

    # Remove busy columns from the count if they fall in a segment
    for c in busy_columns:
        for start, end in segments:
            if start <= c <= end:
                count -= 1
                break
    return count


def first(input: TextIO, row=2_000_000) -> int:
    sensors = parse(input.read())
    return count_impossible_positions_in_row(sensors, row)


def second(input: TextIO, search_space: int = 4_000_000) -> int:
    sensors = parse(input.read())

    sensors_c = [s.pos for s in sensors]
    beacons_c = [s.beacon for s in sensors]

    # This could be much faster by computing segments in the search space for each sensor for each row, _then_
    # merging the segments row by row. But this works and I don't have to write much code.
    for row in range(0, search_space + 1):
        segments = [intersect for s in sensors if (intersect := row_intersect(row, s)) is not None]
        segments = [(max(0, start), min(search_space, end)) for start, end in segments]
        segments.extend([(c, c) for r, c in sensors_c + beacons_c if r == row])
        merged_segments = merge_segments(segments)

        if merged_segments[0][0] == 0 and merged_segments[0][1] == search_space:
            continue

        start, end = merged_segments[0]
        if len(merged_segments) == 2:
            col = end + 1
        else:
            col = 0 if start == 1 else search_space
        return col * 4000000 + row

    raise Exception('🐞')
