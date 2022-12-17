import itertools as it
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field, replace
from typing import Any, Dict, Iterable, Iterator, List, Set, TextIO, Tuple, TypeVar




@dataclass
class Valve:
    name: str
    flow: int
    neighbors: List[str] = field(default_factory=list)


def parse(input: str) -> List[Valve]:
    valves = []
    for line in input.rstrip().splitlines():
        m = re.match(r'^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)$', line)
        if m is None:
            raise Exception('🐞')
        name, rate_s, valves_s = m.groups()
        valves.append(Valve(name=name,
                            flow=int(rate_s),
                            neighbors=valves_s.split(', ')
                            ))
    return valves


@dataclass
class Candidate:
    current: str
    pressure_released: int = 0
    total_flow: int = 0
    open: Set[str] = field(default_factory=set)
    current_elephant: str = None


def next_candidates(vm: Dict[str, Valve], c) -> List[Candidate]:
    next_candidates_list = []
    valve = vm[c.current]

    # Can we open the current valve
    if valve.flow and c.current not in c.open:
        next_candidates_list.append(
            replace(c, open=c.open | {valve.name}, total_flow=c.total_flow + valve.flow))

    # Move options
    for neighbor in valve.neighbors:
        next_candidates_list.append(replace(c, current=neighbor))

    return next_candidates_list


def next_candidates_elephant(vm: Dict[str, Valve], c) -> List[Candidate]:
    next_candidates_list = []
    valve = vm[c.current]
    elephant_valve = vm[c.current_elephant]

    # Can we open the current valve
    if valve.flow and c.current not in c.open:
        # We open and elephant moves
        for neighbor in elephant_valve.neighbors:
            next_candidates_list.append(
                replace(c, current_elephant=neighbor, open=c.open | {valve.name}, total_flow=c.total_flow + valve.flow))

        # Both open
        if elephant_valve.flow and elephant_valve.name not in c.open and c.current_elephant != c.current:
            next_candidates_list.append(
                replace(c, open=c.open | {valve.name, elephant_valve.name},
                        total_flow=c.total_flow + valve.flow + elephant_valve.flow))

    # Move options
    for my_neighbor in valve.neighbors:
        # We move and elephant opens
        if elephant_valve.flow and elephant_valve.name not in c.open:
            next_candidates_list.append(
                replace(c, current=my_neighbor, open=c.open | {elephant_valve.name},
                        total_flow=c.total_flow + elephant_valve.flow))

        # We move and elephant moves
        for elephant_neighbor in elephant_valve.neighbors:
            next_candidates_list.append(replace(c, current=my_neighbor, current_elephant=elephant_neighbor))

    return next_candidates_list


def prune(candidates: List[Candidate], time_left: int, top: int = 100) -> List[Candidate]:
    # We're only going to keep the candidate with the best flow + total per node
    per_node = defaultdict(list)

    for c in candidates:
        score = c.total_flow * time_left + c.pressure_released
        per_node[c.current].append((score, c))

    r = []
    for vals in per_node.values():
        # I don't know why top score isn't the best factor, there's a problem with my heuristic, so instead
        # this is keeping the top `top` results for the node
        r.extend(v[1] for v in sorted(vals, key=lambda x: x[0], reverse=True)[:top])
    return r


def prune_with_elephant(candidates: List[Candidate], time_left: int, top: int = 100) -> List[Candidate]:
    # We're only going to keep the candidate with the best flow + total per node
    per_node = defaultdict(list)

    for c in candidates:
        score = c.total_flow * time_left + c.pressure_released
        k = (c.current, c.current_elephant) if c.current < c.current_elephant else (c.current_elephant, c.current)
        per_node[k].append((score, c))

    r = []
    for vals in per_node.values():
        # Top flow should win in case of draw? Or keep all the top values?
        r.extend(v[1] for v in sorted(vals, key=lambda x: x[0], reverse=True)[:top])
    return r


def optimize_output(valves: List[Valve], elephant: bool = False) -> int:
    vm = {v.name: v for v in valves}

    candidates = [Candidate('AA', current_elephant='AA')]

    for t in range(1, 31):
        if elephant and t <= 4:
            continue

        new_candidates = []
        for c in candidates:
            c.pressure_released += c.total_flow
            if elephant:
                new_candidates += next_candidates_elephant(vm, c)
            else:
                new_candidates += next_candidates(vm, c)

        # print(f't={t}')
        # print(f'Candidates before pruning:\n\t' + '\n\t'.join(str(c) for c in new_candidates))
        if elephant:
            candidates = prune_with_elephant(new_candidates, 30 - t)
        else:
            candidates = prune(new_candidates, 30 - t)
        # print(f'Candidates after pruning:\n\t' + '\n\t'.join(str(c) for c in candidates))

    return max(c.pressure_released for c in candidates)


def compute_distances(valves: List[Valve]) -> Dict[Tuple[str, str], int]:
    """I did not end up using this, but it would have been essential to reaching an optimal solution."""
    distances = {}

    for v in valves:
        distances[(v.name, v.name)] = 0
        for n in v.neighbors:
            distances[(v.name, n)] = 1
            distances[(n, v.name)] = 1
    vm = {v.name: v for v in valves}

    def get_distance(v1n: str, v2n: str, visited: Set[str] = None) -> int | None:
        visited = set(v1n) if visited is None else visited | {v1n}
        d = distances.get((v1n, v2n))
        if d is not None:
            return d

        neighbors = [n for n in vm[v1n].neighbors if n not in visited]
        if not neighbors:
            return None

        distances_from_neighbors = [dd for n in neighbors if (dd := get_distance(n, v2n, visited))]
        if not distances_from_neighbors:
            return None

        d = min(distances_from_neighbors) + 1
        distances[(v1n, v2n)] = d
        distances[(v2n, v1n)] = d
        return d

    [get_distance(a, b) for a, b in it.combinations(vm.keys(), 2)]
    return distances


def first(input: TextIO) -> int:
    valves = parse(input.read())
    return optimize_output(valves)


def second(input: TextIO) -> int:
    valves = parse(input.read())
    return optimize_output(valves, True)
