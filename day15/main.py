import re
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def distance(self, other: 'Coords') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __add__(self, other: 'Coords') -> 'Coords':
        return Coords(self.x + other.x, self.y + other.y)


@dataclass(frozen=True)
class Sensor:
    coords: Coords
    closest_beacon: Coords

    @classmethod
    def create(cls, line: str) -> 'Sensor':
        match = re.match(
            r'^Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): '
            r'closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)$',
            line,
        )
        return Sensor(
            coords=Coords(int(match.group('sensor_x')), int(match.group('sensor_y'))),
            closest_beacon=Coords(int(match.group('beacon_x')), int(match.group('beacon_y'))),
        )

    @property
    @lru_cache
    def distance(self):
        return self.coords.distance(self.closest_beacon)

    def covered_at(self, y: int) -> set[Coords]:
        x_distance = self.distance - abs(self.coords.y - y)
        return {
            Coords(x, y)
            for x in range(self.coords.x - x_distance, self.coords.x + x_distance)
        }

    def to_close(self, location: Coords) -> bool:
        return self.coords.distance(location) <= self.distance

    def get_next(self, location, max_d: int):
        next_x = self.coords.x + self.distance - abs(self.coords.y - location.y)
        if next_x <= max_d:
            return Coords(next_x, location.y)
        else:
            return Coords(0, location.y + 1)

    def as_polygon(self) -> list[Coords]:
        return [
            self.coords + Coords(self.distance, 0),
            self.coords + Coords(-self.distance, 0),
            self.coords + Coords(0, self.distance),
            self.coords + Coords(0, -self.distance),
        ]

    def generate_neighbours(self) -> set[Coords]:
        return {
            coords
            for mix in range(self.distance + 1)
            for coords in {
                # From North to East (East excluded)
                self.coords + Coords(mix, self.distance + 1 - mix),
                # From East to South (South excluded)
                self.coords + Coords(self.distance + 1 - mix, - mix),
                # From South to West (West excluded)
                self.coords + Coords(-mix, - self.distance - 1 + mix),
                # From West to North (North excluded)
                self.coords + Coords(-self.distance - 1 + mix, mix),
            }
        }


def solve(data: str, y: int) -> int:
    sensors = {
        Sensor.create(line)
        for line in data.split('\n')
    }
    covered_coords = {
        coord
        for sensor in sensors
        for coord in sensor.covered_at(y)
    }
    return len(covered_coords)


def solve_gold(data: str, max_d: int):
    sensors: list[Sensor] = [
        Sensor.create(line)
        for line in data.split('\n')
    ]

    sensors.sort(key=lambda sensor: sensor.distance)

    last_other_sensor_to_be_close = sensors[0]
    for sensor in sensors:
        for neighbour in sensor.generate_neighbours():
            if (
                (0 <= neighbour.x <= max_d)
                and
                (0 <= neighbour.y <= max_d)
            ):
                neighbour_covered = False
                if last_other_sensor_to_be_close.to_close(neighbour):
                    neighbour_covered = True
                else:
                    for other_sensor in sensors:
                        if other_sensor.to_close(neighbour):
                            neighbour_covered = True
                            last_other_sensor_to_be_close = other_sensor
                            break
                if not neighbour_covered:
                    return neighbour.x * 4_000_000 + neighbour.y
