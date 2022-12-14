from pathlib import Path

import assertpy
import pytest

from day12.main import solve, Hill, Coords

EXAMPLE = Path('example.txt').read_text()
INPUT = Path('input.txt').read_text()


def test_silver_example():
    assertpy.assert_that(solve(EXAMPLE)).is_equal_to(31)


def test_silver():
    assertpy.assert_that(solve(INPUT)).is_equal_to(528)


def test_gold():
    assertpy.assert_that(
        528  # solution silver
        - 6  # visually from input
    ).is_equal_to(522)


def test_start():
    assertpy.assert_that(Hill(EXAMPLE).start).is_equal_to(Coords(0, 0))


def test_end():
    assertpy.assert_that(Hill(EXAMPLE).end).is_equal_to(Coords(5, 2))


@pytest.mark.parametrize(
    'location,expected',
    [
        (Coords(0, 0), 0),
        (Coords(5, 2), 25),

        (Coords(1, 0), 0),
        (Coords(4, 2), 25),
    ]
)
def test_height_at(location: Coords, expected: int):
    assertpy.assert_that(Hill(EXAMPLE).height_at(location)).is_equal_to(expected)
