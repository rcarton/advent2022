import math
import operator
import re
from collections import deque
from dataclasses import dataclass
from typing import Callable, Deque, List, Optional, TextIO


@dataclass
class Monkey:
    num: int

    items: Deque[int]
    op: Callable[[int], int]
    test_divider: int
    test_true_monkey: int
    test_false_monkey: int

    inspections: int = 0


def turn(monkey_num: int, monkeys: List[Monkey], worry_reduction: Optional[int] = None) -> None:
    monkey = monkeys[monkey_num]

    while monkey.items:
        item = monkey.items.popleft()

        # Inspect
        monkey.inspections += 1
        item = monkey.op(item)

        # Worry reduction
        if worry_reduction is None:
            item //= 3
        else:
            item %= worry_reduction

        # Test then send
        if item % monkey.test_divider == 0:
            monkeys[monkey.test_true_monkey].items.append(item)
        else:
            monkeys[monkey.test_false_monkey].items.append(item)


def round(monkeys: List[Monkey], worry_reduction: Optional[int] = None) -> None:
    for monkey_num in range(len(monkeys)):
        turn(monkey_num, monkeys, worry_reduction=worry_reduction)


def parse_monkey(monkey_s: str) -> Monkey:
    num_s, items_s, op_s, test_s, true_s, false_s = monkey_s.splitlines()
    op_m = re.match(r"^.*Operation: new = old (?P<op>.) (?P<arg2>(\d+|old))", op_s).groupdict()
    op_fn = operator.mul if op_m['op'] == '*' else operator.add
    op = lambda old: op_fn(old, old if op_m['arg2'] == 'old' else int(op_m['arg2']))

    return Monkey(
        num=int(re.match(r"^Monkey (?P<num>\d+):$", num_s).groupdict()['num']),
        items=deque(map(int, re.findall(r"\d+", items_s))),
        op=op,
        test_divider=int(re.search(r"\d+", test_s).group()),
        test_true_monkey=int(re.search(r"\d+", true_s).group()),
        test_false_monkey=int(re.search(r"\d+", false_s).group()),
    )


def first(input: TextIO) -> int:
    monkeys = [parse_monkey(m_s) for m_s in input.read().split('\n\n') if m_s]
    for _ in range(20):
        round(monkeys)

    m1, m2 = sorted([m.inspections for m in monkeys], reverse=True)[:2]
    return m1 * m2


def second(input: TextIO) -> int:
    monkeys = [parse_monkey(m_s) for m_s in input.read().split('\n\n') if m_s]
    worry_reduction = math.lcm(*[m.test_divider for m in monkeys])

    for _ in range(10_000):
        round(monkeys, worry_reduction=worry_reduction)

    m1, m2 = sorted([m.inspections for m in monkeys], reverse=True)[:2]
    return m1 * m2
