from pathlib import Path
from textwrap import dedent

import assertpy
import pytest

from day14.main import solve_silver, Coords, split_path, Cave, solve_gold

EXAMPLE = Path('example.txt').read_text()
INPUT = Path('input.txt').read_text()


def test_silver_example():
    assertpy.assert_that(solve_silver(EXAMPLE)).is_equal_to(24)


def test_silver():
    assertpy.assert_that(solve_silver(INPUT)).is_equal_to(763)


def test_gold_example():
    assertpy.assert_that(solve_gold(EXAMPLE)).is_equal_to(93)


# def test_gold():  # takes 37min20sec
#     assertpy.assert_that(solve_gold(INPUT)).is_equal_to(23921)


@pytest.mark.parametrize(
    'path,coords',
    [
        (
            '498,4 -> 498,6 -> 496,6',
            {
                Coords(498, 4),
                Coords(498, 5),
                Coords(498, 6),
                Coords(497, 6),
                Coords(496, 6),
            },
        ),
        (
            '503,4 -> 502,4 -> 502,9 -> 494,9',
            {
                Coords(503, 4),
                Coords(502, 4),
                Coords(502, 5),
                Coords(502, 6),
                Coords(502, 7),
                Coords(502, 8),
                Coords(502, 9),
                Coords(501, 9),
                Coords(500, 9),
                Coords(499, 9),
                Coords(498, 9),
                Coords(497, 9),
                Coords(496, 9),
                Coords(495, 9),
                Coords(494, 9),
            },
        ),
    ]
)
def test_split_path(path: str, coords: set[Coords]):
    assertpy.assert_that(split_path(path)).contains_only(*coords)


def test_cave_create():
    assertpy.assert_that(
        Cave.create(EXAMPLE).render()[1:]
    ).is_equal_to(
        dedent('''
        ......+...
        ..........
        ..........
        ..........
        ....#...##
        ....#...#.
        ..###...#.
        ........#.
        ........#.
        #########.
        ''').strip('\n')
    )


@pytest.mark.parametrize(
    'count,render',
    [
        (
            1,
            '''
            ......+...
            ..........
            ..........
            ..........
            ....#...##
            ....#...#.
            ..###...#.
            ........#.
            ......o.#.
            #########.
            ''',
        ),
        (
            2,
            '''
            ......+...
            ..........
            ..........
            ..........
            ....#...##
            ....#...#.
            ..###...#.
            ........#.
            .....oo.#.
            #########.
            ''',
        ),
        (
            24,
            '''
            ......+...
            ..........
            ......o...
            .....ooo..
            ....#ooo##
            ...o#ooo#.
            ..###ooo#.
            ....oooo#.
            .o.ooooo#.
            #########.
            ''',
        ),
    ]
)
def test_cave_sand(count: int, render: str):
    assertpy.assert_that(
        Cave.create(EXAMPLE).drop_sand(count).render()[1:]
    ).is_equal_to(
        dedent(render).strip('\n')
    )
