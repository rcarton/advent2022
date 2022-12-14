import itertools as it
from typing import List, TextIO
import json


def compare(left: List | int | None, right: List | int | None) -> int:
    if left is None:
        return -1
    if right is None:
        return 1
    if type(left) == type(right) == int:
        return -1 if left < right else 1 if left > right else 0

    if type(left) == int:
        left = [left]
    if type(right) == int:
        right = [right]

    for l, r in it.zip_longest(left, right):
        if (cmp := compare(l, r)) == -1:
            return -1
        elif cmp == 1:
            return 1
    return 0


def first(input: TextIO) -> int:
    pairs = [map(json.loads, pair.split('\n')) for pair in input.read().rstrip().split('\n\n')]
    return sum(i + 1 for i, p in enumerate(pairs) if compare(*p) == -1)


def merge_sort(packets: List) -> List:
    if (length := len(packets)) < 2:
        return packets
    if length == 2:
        l, r = packets
        return [l, r] if compare(l, r) < 1 else [r, l]

    # We have 2 sorted lists
    left, right = merge_sort(packets[:length // 2]), merge_sort(packets[length // 2:])
    result = []
    while left and right:
        pop_from = left if compare(left[0], right[0]) < 1 else right
        result.append(pop_from.pop(0))
    # Add the rest
    result.extend(left)
    result.extend(right)
    return result


def merge_sort_in_place(packets: List, start: int | None = None, end: int | None = None) -> None:
    """
    start is inclusive, end is exclusive
    """
    if start is None:
        start = 0
    if end is None:
        end = len(packets)

    if (length := end - start) < 2:
        # Nothing to do, already in order since 1 or 0 elements
        return

    if length == 2:
        if compare(packets[start], packets[start + 1]) == 1:
            # Swap
            packets[start], packets[start + 1] = packets[start + 1], packets[start]
        return

    pivot = start + ((end - start) // 2)
    merge_sort_in_place(packets, start, pivot)
    merge_sort_in_place(packets, pivot, end)

    # Now we're merging 2 sorted arrays in place, n * m complexity
    for left_i in range(start, pivot):
        if compare(packets[left_i], packets[pivot]) == 1:
            packets[left_i], packets[pivot] = packets[pivot], packets[left_i]

            # The right side may be out of order now, gotta swap until in order
            for right_i in range(pivot, end - 1):
                if compare(packets[right_i], packets[right_i + 1]) == 1:
                    packets[right_i], packets[right_i + 1] = packets[right_i + 1], packets[right_i]


def quicksort(packets: List) -> List:
    if (length := len(packets)) < 2:
        return packets
    pivot_i = length // 2
    left = []
    right = []
    for i, n in enumerate(packets):
        if i == pivot_i:
            continue
        if compare(n, packets[pivot_i]) < 1:
            left.append(n)
        else:
            right.append(n)
    return quicksort(left) + [packets[pivot_i]] + quicksort(right)


def second(input: TextIO) -> int:
    packets = [json.loads(line) for line in input.read().rstrip().split('\n') if line]
    # Add the 2 divider packets
    divider_packets = [
        [[2]],
        [[6]]
    ]
    packets.extend(divider_packets)
    # packets = merge_sort(packets)
    # merge_sort_in_place(packets)
    packets = quicksort(packets)
    divider_packet_indices = [i + 1 for i, p in enumerate(packets) if p in divider_packets]
    return divider_packet_indices[0] * divider_packet_indices[1]
