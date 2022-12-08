import abc
import itertools as it
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Deque, Dict, Iterable, Iterator, List, TextIO, Tuple, TypeVar

import typing


@dataclass
class Node(abc.ABC):
    __metaclass__ = abc.ABCMeta

    name: str

    @abc.abstractmethod
    def get_size(self) -> int:
        raise Exception("Not implemented")


@dataclass
class Dir(Node):
    parent: typing.Optional['Dir']
    content: Dict[str, Node] = field(default_factory=dict)

    def get_size(self) -> int:
        return sum(n.get_size() for n in self.content.values())


@dataclass
class File(Node):
    size: int

    def get_size(self) -> int:
        return self.size


def parse_ls(current_node: Node, lines: Deque[str]) -> None:
    while lines:
        line = lines.popleft()

        # Done parsing ls
        if line.startswith('$ '):
            lines.appendleft(line)
            return

    return


def parse_command(current_dir: Dir, cmd_s: str) -> Dir:
    cmd_line, *output = [i for i in cmd_s.split('\n') if i]

    cmd, *args = cmd_line.split(' ')
    if cmd == 'cd':
        next_dir = current_dir.content[args[0]] if args[0] != '..' else current_dir.parent
        if type(next_dir) != Dir:
            raise Exception(f'Invalid type for {args[0]}: not a dir')
        return typing.cast(Dir, next_dir)
    if cmd == 'ls':
        # Parse the output and build the tree
        for o in output:
            left, filename = o.split(' ')
            if left == 'dir':
                current_dir.content[filename] = Dir(name=filename, parent=current_dir)
            else:
                current_dir.content[filename] = File(name=filename, size=int(left))
        return current_dir
    else:
        raise Exception(f'Unknown cmd={cmd}')


def parse(output: str) -> Dir:
    commands_with_output = deque([l for l in output.split('$ ') if l])

    # The output starts with `$ cd /`
    commands_with_output.popleft()
    filesystem = Dir(name='/', parent=None)
    current_dir: Dir = filesystem

    for cmd_s in commands_with_output:
        current_dir = parse_command(current_dir, cmd_s)

    return filesystem


def first(input: TextIO) -> int:
    fs = parse(input.read())

    # We have the full filesystem, now we need to do a traversal to find all the directories with size < 100_000
    dirs_to_visit = deque([fs])
    small_dirs = []
    while dirs_to_visit:
        curr = dirs_to_visit.pop()
        if curr.get_size() <= 100_000:
            small_dirs.append(curr)
        dirs_to_visit.extend(typing.cast(Dir, d) for d in curr.content.values() if type(d) == Dir)

    return sum(d.get_size() for d in small_dirs)


def second(input: TextIO) -> int:
    fs = parse(input.read())
    fs_size_total = 70_000_000
    fs_free_space_required = 30_000_000
    fs_size_needed = fs_free_space_required - (fs_size_total - fs.get_size())

    # Same as first but we want dirs with at least fs_size_needed
    dirs_to_visit = deque([fs])
    big_dirs = []
    while dirs_to_visit:
        curr = dirs_to_visit.pop()
        if curr.get_size() >= fs_size_needed:
            big_dirs.append(curr)
        dirs_to_visit.extend(typing.cast(Dir, d) for d in curr.content.values() if type(d) == Dir)

    # Sort by size, smallest first
    big_dirs = sorted(big_dirs, key=lambda d: d.get_size())

    return big_dirs[0].get_size()
