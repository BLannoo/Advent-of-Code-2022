from pathlib import Path

import assertpy

from day16.main import solve, Valve, all_distances, pressure_released, \
    create_distances_matrix_of_valves_with_flow

EXAMPLE = Path('example.txt').read_text()
INPUT = Path('input.txt').read_text()


def test_silver_example():
    assertpy.assert_that(solve(EXAMPLE)).is_equal_to(1651)


# def test_silver():
#     assertpy.assert_that(solve(INPUT)).is_equal_to(1651)


def test_all_distances():
    assertpy.assert_that(
        all_distances('AA', Valve.parse_all(EXAMPLE))
    ).is_equal_to(
        {
            'AA': 0,
            'BB': 1,
            'CC': 2,
            'DD': 1,
            'EE': 2,
            'FF': 3,
            'GG': 4,
            'HH': 5,
            'II': 1,
            'JJ': 2,
        }
    )


def test_pressure_released():
    valves = Valve.parse_all(EXAMPLE)
    distances_matrix = create_distances_matrix_of_valves_with_flow(valves)
    assertpy.assert_that(
        pressure_released(
            path=('DD', 'BB', 'JJ', 'HH', 'EE', 'CC'),
            distances_matrix=distances_matrix,
            valves=valves,
        )
    ).is_equal_to(
        1651
    )
