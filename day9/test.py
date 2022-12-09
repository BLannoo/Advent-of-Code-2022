from pathlib import Path

import assertpy
import pytest

from day9.main import solve, Coords

EXAMPLE = Path('example.txt').read_text()
LARGER_EXAMPLE = Path('larger_example.txt').read_text()
INPUT = Path('input.txt').read_text()


def test_silver_example():
    assertpy.assert_that(solve(EXAMPLE)).is_equal_to(13)


def test_silver():
    assertpy.assert_that(solve(INPUT)).is_equal_to(5619)


def test_gold_example():
    assertpy.assert_that(solve(EXAMPLE, tail_count=9)).is_equal_to(1)


def test_gold_larger_example():
    assertpy.assert_that(solve(LARGER_EXAMPLE, tail_count=9)).is_equal_to(36)


def test_gold():
    assertpy.assert_that(solve(INPUT, tail_count=9)).is_equal_to(2376)


@pytest.mark.parametrize(
    'commands,visited',
    [
        ('R 1', 1),
        ('R 2', 2),
        ('R 3', 3),
        ('L 1', 1),
        ('L 2', 2),
        ('L 3', 3),
        ('R 1\nL 1', 1),
        ('R 1\nL 2', 1),
        ('R 1\nL 3', 2),
        ('U 1', 1),
        ('U 2', 2),
        ('U 3', 3),
        ('D 1', 1),
        ('D 2', 2),
        ('D 3', 3),
        ('R 1\nU 2', 2),
    ]
)
def test_small_examples(commands: str, visited: int):
    assertpy.assert_that(solve(commands)).is_equal_to(visited)


@pytest.mark.parametrize(
    'start,direction,end',
    [
        (Coords(0, 0), 'R', Coords(1, 0)),
        (Coords(0, 0), 'L', Coords(-1, 0)),
        (Coords(0, 0), 'U', Coords(0, 1)),
        (Coords(0, 0), 'D', Coords(0, -1)),
    ]
)
def test_coordinates_move(start: Coords, direction: str, end: Coords):
    assertpy.assert_that(start.move(direction)).is_equal_to(end)


@pytest.mark.parametrize(
    'head,tail_before,tail_after',
    [
        (Coords(0, 0), Coords(0, 0), Coords(0, 0)),

        # L & R
        (Coords(0, 0), Coords(1, 0), Coords(1, 0)),
        (Coords(0, 0), Coords(2, 0), Coords(1, 0)),
        (Coords(0, 0), Coords(-2, 0), Coords(-1, 0)),

        # U & D
        (Coords(0, 0), Coords(0, 1), Coords(0, 1)),
        (Coords(0, 0), Coords(0, 2), Coords(0, 1)),
        (Coords(0, 0), Coords(0, -2), Coords(0, -1)),

        # Full diagonal
        (Coords(0, 0), Coords(2, 2), Coords(1, 1)),
        (Coords(0, 0), Coords(-2, 2), Coords(-1, 1)),
        (Coords(0, 0), Coords(2, -2), Coords(1, -1)),
        (Coords(0, 0), Coords(-2, -2), Coords(-1, -1)),

        # Partial diagonal
        (Coords(0, 0), Coords(2, 1), Coords(1, 0)),
        (Coords(0, 0), Coords(1, 2), Coords(0, 1)),
        (Coords(0, 0), Coords(2, -1), Coords(1, 0)),
        (Coords(0, 0), Coords(1, -2), Coords(0, -1)),
        (Coords(0, 0), Coords(-2, -1), Coords(-1, 0)),
        (Coords(0, 0), Coords(-1, -2), Coords(0, -1)),
        (Coords(0, 0), Coords(-2, 1), Coords(-1, 0)),
        (Coords(0, 0), Coords(-1, 2), Coords(0, 1)),
    ]
)
def test_coordinates_follow(head: Coords, tail_before: Coords, tail_after: Coords):
    assertpy.assert_that(tail_before.follow(head)).is_equal_to(tail_after)
