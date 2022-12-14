import bisect
from dataclasses import dataclass, field
from functools import lru_cache


@dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: 'Coords') -> 'Coords':
        return Coords(self.x + other.x, self.y + other.y)

    def manhattan_distance(self, other: 'Coords') -> float:
        return abs(self.x - other.x) + abs(self.y - other.y)


DIRECTIONS = (
    Coords(1, 0),
    Coords(-1, 0),
    Coords(0, 1),
    Coords(0, -1),
)


@dataclass(frozen=True)
class Hill:
    data: str

    @property
    @lru_cache
    def width(self):
        return len(self.data.split('\n')[0])

    @property
    @lru_cache
    def height(self):
        return len(self.data.split('\n'))

    @property
    @lru_cache
    def start(self) -> Coords:
        return self._find('S')

    @property
    @lru_cache
    def end(self) -> Coords:
        return self._find('E')

    @lru_cache
    def _find(self, char: str) -> Coords:
        index = self._pure_data().index(char)
        return Coords(
            x=index % self.width,
            y=index // self.width,
        )

    @lru_cache
    def height_at(self, location: Coords) -> int:
        letter = self.letter_at(location)
        if letter == 'S':
            return 0
        if letter == 'E':
            return 25
        return ord(letter) - ord('a')

    def letter_at(self, location: Coords) -> str:
        return self._pure_data()[location.y * self.width + location.x]

    @lru_cache
    def _pure_data(self):
        return self.data.replace('\n', '')

    @lru_cache
    def contains(self, location: Coords) -> bool:
        return (
            (0 <= location.x < self.width)
            and
            (0 <= location.y < self.height)
        )

    @lru_cache
    def heuristic(self, path: tuple[Coords]) -> float:
        distance_to_end = self.end.manhattan_distance(path[-1])
        return len(path)  # + max(distance_to_end, 25 - self.height)


@dataclass(frozen=True, order=True)
class Partial:
    heuristic: float
    path: tuple[Coords] = field(compare=False)

    @classmethod
    def from_path_and_hill(cls, path: tuple[Coords], hill: Hill) -> 'Partial':
        return Partial(path=path, heuristic=hill.heuristic(path))

    def add(self, location: Coords, hill: Hill) -> 'Partial':
        return Partial.from_path_and_hill(
            (*self.path, location),
            hill,
        )

    def render(self, hill: Hill):
        print()
        for y in range(hill.height):
            for x in range(hill.width):
                location = Coords(x, y)
                if location in self.path:
                    print('#', end='')
                else:
                    print(hill.letter_at(location), end='')
            print()


def solve(data: str) -> int:
    hill = Hill(data)
    partial_paths = [Partial.from_path_and_hill((hill.start,), hill)]
    visited = {hill.start}
    while len(partial_paths) > 0:
        current_partial_path = partial_paths.pop(0)
        current_height = hill.height_at(current_partial_path.path[-1])
        for direction in DIRECTIONS:
            next_step = current_partial_path.path[-1] + direction
            if (
                (not hill.contains(next_step))
                or
                (next_step in visited)
            ):
                continue
            height = hill.height_at(next_step)
            if height <= current_height + 1:
                if next_step == hill.end:
                    current_partial_path.render(hill)
                    return len(current_partial_path.path)
                new_partial_path = current_partial_path.add(next_step, hill)
                visited.add(next_step)
                bisect.insort(partial_paths, new_partial_path)

    return 0
