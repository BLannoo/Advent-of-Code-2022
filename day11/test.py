import textwrap
from pathlib import Path

import assertpy
import pytest

from day11.main import solve_silver, parse, execute_round, calculate_worry_modulo, solve_gold
from day11.test_utils import monkeys_test_builder, monkeys_printer, inspections_printer

EXAMPLE = Path('example.txt').read_text()
INPUT = Path('input.txt').read_text()


def test_silver_example():
    assertpy.assert_that(solve_silver(EXAMPLE)).is_equal_to(10605)


def test_silver():
    assertpy.assert_that(solve_silver(INPUT)).is_equal_to(100345)


def test_gold_example():
    assertpy.assert_that(solve_gold(EXAMPLE)).is_equal_to(2713310158)


def test_gold():
    assertpy.assert_that(solve_gold(INPUT)).is_equal_to(28537348205)


def test_parse():
    assertpy.assert_that(
        parse(EXAMPLE)
    ).contains_only(
        *monkeys_test_builder()
    )


def test_process_next_item():
    monkeys = monkeys_test_builder()
    assertpy.assert_that(monkeys[0].process_next_item()).is_equal_to((3, 500))
    assertpy.assert_that(monkeys[0].process_next_item()).is_equal_to((3, 620))

    assertpy.assert_that(monkeys[1].process_next_item()).is_equal_to((0, 20))
    assertpy.assert_that(monkeys[1].process_next_item()).is_equal_to((0, 23))
    assertpy.assert_that(monkeys[1].process_next_item()).is_equal_to((0, 27))
    assertpy.assert_that(monkeys[1].process_next_item()).is_equal_to((0, 26))

    assertpy.assert_that(monkeys[2].process_next_item()).is_equal_to((1, 2080))
    assertpy.assert_that(monkeys[2].process_next_item()).is_equal_to((3, 1200))
    assertpy.assert_that(monkeys[2].process_next_item()).is_equal_to((3, 3136))

    assertpy.assert_that(monkeys[3].process_next_item()).is_equal_to((1, 25))


@pytest.mark.parametrize(
    'rounds,summary',
    [
        (
            1,
            '''
            Monkey 0: 20, 23, 27, 26
            Monkey 1: 2080, 25, 167, 207, 401, 1046
            Monkey 2: 
            Monkey 3: 
            '''
        ),
        (
            2,
            '''
            Monkey 0: 695, 10, 71, 135, 350
            Monkey 1: 43, 49, 58, 55, 362
            Monkey 2: 
            Monkey 3: 
            '''
        ),
        (
            20,
            '''
            Monkey 0: 10, 12, 14, 26, 34
            Monkey 1: 245, 93, 53, 199, 115
            Monkey 2: 
            Monkey 3: 
            '''
        ),
    ]
)
def test_execute_round(rounds: int, summary: str):
    monkeys = monkeys_test_builder()
    for _ in range(rounds):
        execute_round(monkeys)
    assertpy.assert_that(monkeys_printer(monkeys)).is_equal_to(
        textwrap.dedent(summary).strip('\n ')
    )


def test_inspected():
    monkeys = monkeys_test_builder()
    for _ in range(20):
        execute_round(monkeys)
    assertpy.assert_that(
        monkeys
    ).extracting(
        'inspected'
    ).is_equal_to(
        [101, 95, 7, 105]
    )


@pytest.mark.parametrize(
    'rounds,expected',
    [
        (
            1,
            '''
            Monkey 0 inspected items 2 times.
            Monkey 1 inspected items 4 times.
            Monkey 2 inspected items 3 times.
            Monkey 3 inspected items 6 times.
            '''
        ),
        (
            20,
            '''
            Monkey 0 inspected items 99 times.
            Monkey 1 inspected items 97 times.
            Monkey 2 inspected items 8 times.
            Monkey 3 inspected items 103 times.
            '''
        ),
        (
            1000,
            '''
            Monkey 0 inspected items 5204 times.
            Monkey 1 inspected items 4792 times.
            Monkey 2 inspected items 199 times.
            Monkey 3 inspected items 5192 times.
            '''
        ),
        (
            10000,
            '''
            Monkey 0 inspected items 52166 times.
            Monkey 1 inspected items 47830 times.
            Monkey 2 inspected items 1938 times.
            Monkey 3 inspected items 52013 times.
            '''
        ),
    ]
)
def test_inspections(rounds: int, expected: str):
    monkeys = monkeys_test_builder()
    worry_modulo = calculate_worry_modulo(monkeys)
    for _ in range(rounds):
        execute_round(monkeys, worry_modulo=worry_modulo, with_relief=False)
    assertpy.assert_that(inspections_printer(monkeys)).is_equal_to(
        textwrap.dedent(expected).strip('\n ')
    )
