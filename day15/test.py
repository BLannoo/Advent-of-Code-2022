from pathlib import Path

import assertpy
import pytest as pytest

from day15.main import solve, solve_gold, Sensor, Coords

EXAMPLE = Path('example.txt').read_text()
INPUT = Path('input.txt').read_text()


def test_silver_example():
    assertpy.assert_that(solve(EXAMPLE, 10)).is_equal_to(26)


def test_silver():
    assertpy.assert_that(solve(INPUT, 2_000_000)).is_equal_to(4_560_025)


def test_gold_example():
    assertpy.assert_that(solve_gold(EXAMPLE, max_d=20)).is_equal_to(56000011)


# def test_gold():  # Takes ~10min
#     assertpy.assert_that(solve_gold(INPUT, max_d=4_000_000)).is_equal_to(12480406634249)


@pytest.mark.parametrize(
    'sensor,neighbours',
    [
        (
            Sensor(Coords(0, 0), closest_beacon=Coords(0, 0)),
            {
                Coords(0, 1),
                Coords(1, 0),
                Coords(0, -1),
                Coords(-1, 0),
            }
        ),
        (
            Sensor(Coords(0, 0), closest_beacon=Coords(1, 0)),
            {
                Coords(0, 2),
                Coords(1, 1),
                Coords(2, 0),
                Coords(1, -1),
                Coords(0, -2),
                Coords(-1, -1),
                Coords(-2, 0),
                Coords(-1, 1),
            }
        ),
    ]
)
def test_generate_neighbours(sensor: Sensor, neighbours: set[Coords]):
    assertpy.assert_that(
        sensor.generate_neighbours()
    ).contains_only(
        *neighbours
    )
