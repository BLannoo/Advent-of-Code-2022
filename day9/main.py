import math
from dataclasses import dataclass


def sign(val: int) -> int:
    return int(math.copysign(1, val))


@dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def move(self, direction: str) -> 'Coords':
        return Coords(self.x, self.y) + DIRECTIONS_TO_DIFFS[direction]

    def follow(self, head: 'Coords') -> 'Coords':
        if abs(self.x - head.x) > 1:
            shift_x = sign(head.x - self.x)
            if self.y != head.y:
                shift_y = sign(head.y - self.y)
            else:
                shift_y = 0
            return Coords(self.x + shift_x, self.y + shift_y)
        elif abs(self.y - head.y) > 1:
            shift_y = sign(head.y - self.y)
            if self.x != head.x:
                shift_x = sign(head.x - self.x)
            else:
                shift_x = 0
            return Coords(self.x + shift_x, self.y + shift_y)
        return self

    def __add__(self, other: 'Coords') -> 'Coords':
        return Coords(self.x + other.x, self.y + other.y)


def solve(data: str, tail_count: int = 1) -> int:
    head = Coords(0, 0)
    tails = [
        Coords(0, 0)
        for _ in range(tail_count)
    ]
    last_tail_locations = {tails[-1]}
    for command in data.split('\n'):
        direction, distance = parse_command(command)
        for _ in range(distance):
            head = head.move(direction)
            tails = move_tails(head, tails)
            last_tail_locations.add(tails[-1])
    return len(last_tail_locations)


def parse_command(command):
    command_parts = command.split(' ')
    assert len(command_parts) == 2
    direction = command_parts[0]
    distance = int(command_parts[1])
    return direction, distance


def move_tails(head, tails):
    previous_tail = head
    new_tails = []
    for tail in tails:
        new_tail = tail.follow(previous_tail)
        new_tails.append(new_tail)
        previous_tail = new_tail
    tails = new_tails
    return tails


DIRECTIONS_TO_DIFFS = {
    'R': Coords(1, 0),
    'L': Coords(-1, 0),
    'U': Coords(0, 1),
    'D': Coords(0, -1),
}
