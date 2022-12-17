import math
from dataclasses import dataclass, field
from functools import lru_cache


@dataclass(frozen=True)
class Coords:
    x: int
    y: int

    @classmethod
    def from_description(cls, description: str) -> 'Coords':
        parts = description.split(',')
        assert len(parts) == 2
        return Coords(int(parts[0]), int(parts[1]))

    def __add__(self, other: 'Coords') -> 'Coords':
        return Coords(self.x + other.x, self.y + other.y)


class SandDone(Exception):
    pass


@dataclass
class Cave:
    rock: tuple[Coords]
    source: Coords = Coords(500, 0)
    sand: set[Coords] = field(default_factory=set)

    @classmethod
    def create(cls, data: str) -> 'Cave':
        rock_locations = tuple(
            coords
            for path in data.split('\n')
            for coords in split_path(path)
        )
        return Cave(
            rock=rock_locations,
        )

    def render(self) -> str:
        render = '\n'
        for y in range(max_y(self.rock) + 1):
            for x in range(min_x(self.rock), max_x(self.rock) + 1):
                if Coords(x, y) in self.sand:
                    render += 'o'
                elif Coords(x, y) == self.source:
                    render += '+'
                elif Coords(x, y) in self.rock:
                    render += '#'
                else:
                    render += '.'
            render += '\n'
        return render[:-1]

    def drop_sand(self, count: int) -> 'Cave':
        for _ in range(count):
            self.drop_single_sand()
        return self

    def drop_single_sand(self) -> 'Cave':
        max_y_val = max_y(self.rock)
        sand = self.source
        has_come_to_rest = False
        while not has_come_to_rest:
            sand_after = self.move(sand)
            if sand_after.y > max_y_val:
                raise SandDone()
            if sand == sand_after:
                has_come_to_rest = True
            else:
                sand = sand_after
        self.sand.add(sand)
        if sand.y == 0:
            raise SandDone()
        return self

    def move(self, sand: Coords) -> Coords:
        for diff in (Coords(0, 1), Coords(-1, 1), Coords(1, 1)):
            next = sand + diff
            if self.is_air(next):
                return next
        return sand

    def is_air(self, coords: Coords) -> bool:
        if coords == self.source:
            return False
        elif coords in self.sand:
            return False
        elif coords in self.rock:
            return False
        else:
            return True

    def add_floor(self):
        max_y_value = max_y(self.rock)
        floor = tuple(
            Coords(x, max_y_value + 2)
            for x in range(
                self.source.x - max_y_value - 3,
                self.source.x + max_y_value + 3,
            )
        )
        self.rock = self.rock + floor


@lru_cache
def max_y(rock: tuple[Coords]):
    return max(
        rock,
        key=lambda location: location.y
    ).y


@lru_cache
def min_x(rock: tuple[Coords]):
    return min(
        rock,
        key=lambda location: location.x
    ).x


@lru_cache
def max_x(rock: tuple[Coords]):
    return max(
        rock,
        key=lambda location: location.x
    ).x


def solve_silver(data: str) -> int:
    cave = Cave.create(data)

    while True:
        try:
            cave.drop_single_sand()
        except SandDone as e:
            return len(cave.sand)


def solve_gold(data: str) -> int:
    cave = Cave.create(data)
    cave.add_floor()

    while True:
        try:
            cave.drop_single_sand()
        except SandDone as e:
            print(cave.render())
            return len(cave.sand)


def split_path(path: str) -> set[Coords]:
    nodes = path.split(' -> ')
    coords = set()
    for i in range(len(nodes) - 1):
        start_node = Coords.from_description(nodes[i])
        end_node = Coords.from_description(nodes[i + 1])
        x_sign = sign(end_node.x - start_node.x)
        for x in range(start_node.x, end_node.x + x_sign, x_sign):
            y_sign = sign(end_node.y - start_node.y)
            for y in range(start_node.y, end_node.y + y_sign, y_sign):
                coords.add(Coords(x, y))
    return coords


def sign(val: int) -> int:
    return int(math.copysign(1, val))
