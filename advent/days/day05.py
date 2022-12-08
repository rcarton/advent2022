import itertools as it
import re
from collections import deque
from dataclasses import dataclass
from typing import Iterable, Iterator, TextIO, Tuple, TypeVar, List


@dataclass
class Stack:
    crates: deque[str]

    def pop(self) -> str:
        return self.crates.pop()


@dataclass()
class Move:
    count: int
    fr: int
    to: int


def move(from_s: Stack, to_s: Stack, count: int) -> None:
    for _ in range(count):
        to_s.crates.append(from_s.crates.pop())


def move2(from_s: Stack, to_s: Stack, count: int) -> None:
    to_s.crates.extend([from_s.crates.pop() for _ in range(count)][::-1])


def parse(input: TextIO) -> Tuple[List[Stack], List[Move]]:
    stacks_s, moves_s = input.read().split('\n\n')

    # Remove the last line, it indicates the stack number
    stacks_s = [s for s in stacks_s.split('\n') if s][:-1]
    moves_s = [m for m in moves_s.split('\n') if m]

    # Keep only the crates + empty string for no crate
    stacks_s = [l[1::4] for l in stacks_s]
    stacks = [Stack(deque([crate for crate in crates if crate.strip()][::-1])) for crates in zip(*stacks_s)]

    moves = [Move(count=int(c), fr=int(f), to=int(t)) for c, f, t in [re.findall(r'\d+', m) for m in moves_s if m]]

    return stacks, moves


def first(input: TextIO) -> str:
    stacks, moves = parse(input)

    for m in moves:
        move(stacks[m.fr - 1], stacks[m.to - 1], m.count)
    return ''.join(s.pop() for s in stacks)


def second(input: TextIO) -> str:
    stacks, moves = parse(input)

    for m in moves:
        move2(stacks[m.fr - 1], stacks[m.to - 1], m.count)
    return ''.join(s.pop() for s in stacks)
