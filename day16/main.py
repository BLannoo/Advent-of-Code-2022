import bisect
import itertools
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Valve:
    name: str
    rate: int
    tunnels: tuple[str]

    @classmethod
    def parse_all(cls, data: str) -> dict[str, 'Valve']:
        valves = [
            Valve.parse(description)
            for description in data.split('\n')
        ]
        return {
            valve.name: valve
            for valve in valves
        }

    @classmethod
    def parse(cls, description: str) -> 'Valve':
        match = re.match(
            r'^Valve (?P<name>\w+) has flow rate=(?P<rate>\d+); '
            r'tunnels? leads? to valves? (?P<tunnels>(\w+,? ?)+)$',
            description,
        )
        return Valve(
            match.group('name'),
            int(match.group('rate')),
            tuple(match.group('tunnels').split(', ')),
        )


@dataclass(frozen=True, order=True)
class Partial:
    max_that_could_be_released: int
    visited: tuple[str, ...]
    released: int
    releasing: int
    time_spend: int

    def generate_new_partials(
        self,
        valves: dict[str, 'Valve'],
        distances_matrix: dict[str, dict[str, int]],
        valves_with_flow: tuple[str],
        total_pressure: int,
        total_time: int,
    ) -> list['Partial']:
        next_valves = tuple(set(valves_with_flow) - set(self.visited))
        return [
            self.new_partial(next_valve, valves, distances_matrix, total_pressure, total_time)
            for next_valve in next_valves
        ]

    def new_partial(
        self,
        next_valve: str,
        valves: dict[str, 'Valve'],
        distances_matrix: dict[str, dict[str, int]],
        total_pressure: int,
        total_time: int,
    ) -> 'Partial':
        distance = distances_matrix[self.visited[-1]][next_valve]
        released = self.released + (distance + 1) * self.releasing
        time_spend = self.time_spend + distance + 1
        releasing = self.releasing + valves[next_valve].rate
        max_that_could_be_released = released + (total_time - time_spend) * (total_pressure - releasing)
        return Partial(
            max_that_could_be_released=max_that_could_be_released,
            visited=(*self.visited, next_valve),
            released=released,
            releasing=releasing,
            time_spend=time_spend,
        )


def solve(data: str, total_time: int = 30) -> int:
    valves = Valve.parse_all(data)
    distances_matrix = create_distances_matrix_of_valves_with_flow(valves)

    valves_with_flow = tuple(
        valve_name
        for valve_name, valve in valves.items()
        if valve.rate > 0
    )

    total_pressure = sum(map(lambda valve: valve.rate, valves.values()))
    print(total_pressure)

    partials = [
        Partial(
            max_that_could_be_released=total_pressure * total_time,
            visited=('AA',), released=0, releasing=0, time_spend=0
        )
    ]
    while len(partials) > 0:
        partial = partials.pop()
        for new_partial in partial.generate_new_partials(
            valves, distances_matrix, valves_with_flow, total_pressure, total_time
        ):
            bisect.insort(partials, new_partial)
    return 0
    # return max(
    #     pressure_released(path, distances_matrix, valves)
    #     for path in itertools.permutations(valves_with_flow)
    # )


def create_distances_matrix_of_valves_with_flow(valves: dict[str, 'Valve']) -> dict[str, dict[str, int]]:
    return {
        valve_name: all_distances(valve_name, valves)
        for valve_name in valves.keys()
    }


def all_distances(valve_name: str, valves: dict[str, 'Valve']) -> dict[str: int]:
    result = {}
    visited_valves: list[str] = []
    next_valves: list[str] = [valve_name]
    steps = 0

    while len(next_valves) > 0:
        result.update({
            next_valve: steps
            for next_valve in next_valves
        })
        visited_valves.extend(next_valves)
        next_valves = [
            next_tunnel
            for current_valve in next_valves
            for next_tunnel in valves[current_valve].tunnels
            if next_tunnel not in visited_valves
        ]
        steps += 1

    return result


def pressure_released(
    path: tuple[str, ...],
    distances_matrix: dict[str, dict[str, int]],
    valves: dict[str, 'Valve']
) -> int:
    current_valve = 'AA'
    result = 0
    time_left = 30
    releasing_pressure = 0
    for next_valve in path:
        distance = distances_matrix[current_valve][next_valve]
        result += (distance + 1) * releasing_pressure
        time_left -= distance + 1
        releasing_pressure += valves[next_valve].rate
        current_valve = path[0]
        path = path[1:]

    result += time_left * releasing_pressure

    return result
