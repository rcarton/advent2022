from dataclasses import dataclass
from typing import TextIO


@dataclass
class Machine:
    cycle: int = 0
    x: int = 1

    interesting_signal_strengths = []
    output = ''

    def start_cycle(self):
        self.update_output()
        self.cycle += 1
        if self.cycle in {20, 60, 100, 140, 180, 220}:
            self.interesting_signal_strengths.append(self.cycle * self.x)

    def update_output(self):
        current_pixel = self.cycle % 40
        overlap = abs(self.x - current_pixel) <= 1
        self.output += '#' if overlap else '.'

        if (self.cycle + 1) % 40 == 0:
            self.output += '\n'

    def run(self: 'Machine', instruction: str) -> None:
        self.start_cycle()
        if instruction.startswith('addx'):
            self.start_cycle()
            self.x += int(instruction.split(' ')[1])


def first(input: TextIO) -> int:
    machine = Machine()
    for instruction in input.read().splitlines():
        machine.run(instruction)
    return sum(machine.interesting_signal_strengths)


def second(input: TextIO) -> int:
    machine = Machine()
    for instruction in input.read().splitlines():
        machine.run(instruction)
    print('\n')
    print(machine.output)
    return -1
