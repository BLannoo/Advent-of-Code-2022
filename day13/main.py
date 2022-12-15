import itertools
from functools import cmp_to_key
from pathlib import Path
from pprint import pprint
from textwrap import dedent
from typing import Optional

import assertpy
import pytest

EXAMPLE = Path('example.txt').read_text()
INPUT = Path('input.txt').read_text()


def test_silver_example():
    assertpy.assert_that(solve_silver(EXAMPLE)).is_equal_to(13)


def test_silver():
    assertpy.assert_that(solve_silver(INPUT)).is_equal_to(6369)


def test_gold_example():
    assertpy.assert_that(solve_gold(EXAMPLE)).is_equal_to(140)


def test_gold():
    assertpy.assert_that(solve_gold(INPUT)).is_equal_to(25800)


@pytest.mark.parametrize(
    'pair,expected',
    [
        (
            '''
            [1,1,3,1,1]
            [1,1,5,1,1]
            ''',
            True,
        ),
        (
            '''
            [[1],[2,3,4]]
            [[1],4]
            ''',
            True,
        ),
        (
            '''
            [9]
            [[8,7,6]]
            ''',
            False,
        ),
        (
            '''
            [[4,4],4,4]
            [[4,4],4,4,4]
            ''',
            True,
        ),
        (
            '''
            [7,7,7,7]
            [7,7,7]
            ''',
            False,
        ),
        (
            '''
            []
            [3]
            ''',
            True,
        ),
        (
            '''
            [[[]]]
            [[]]
            ''',
            False,
        ),
        (
            '''
            [1,[2,[3,[4,[5,6,7]]]],8,9]
            [1,[2,[3,[4,[5,6,0]]]],8,9]
            ''',
            False,
        ),
        (
            '''
            [[]]
            [1]
            ''',
            True,
        ),
        (
            '''
            [1]
            [[]]
            ''',
            False,
        ),
    ]
)
def test_is_in_the_right_order(pair: str, expected: bool):
    pair = dedent(pair).strip('\n')
    assertpy.assert_that(is_in_the_right_order(pair)).is_equal_to(expected)


def solve_silver(data: str) -> int:
    pairs = data.split('\n\n')
    return sum(
        index + 1
        for index, pair in enumerate(pairs)
        if is_in_the_right_order(pair)
    )


def solve_gold(data: str) -> int:
    packets = [
        eval(packet)
        for packet in data.split('\n')
        if packet != ''
    ]
    divider_packet_1 = [[2]]
    divider_packet_2 = [[6]]
    packets.append(divider_packet_1)
    packets.append(divider_packet_2)

    packets.sort(key=cmp_to_key(is_in_the_right_order_given_two_lists), reverse=True)

    pprint(packets)

    return (packets.index(divider_packet_1) + 1) * (packets.index(divider_packet_2) + 1)


def is_in_the_right_order(pair: str) -> bool:
    pairs = pair.split('\n')
    assert len(pairs) == 2
    left_list = eval(pairs[0])
    right_list = eval(pairs[1])
    if isinstance(left_list, list) and isinstance(right_list, list):
        if 1 == is_in_the_right_order_given_two_lists(left_list, right_list):
            return True
        else:
            return False


def is_in_the_right_order_given_two_lists(left_list: list, right_list) -> int:
    for left_element, right_element in itertools.zip_longest(left_list, right_list):

        if (left_element is None) and (right_element is not None):
            return 1
        if (left_element is not None) and (right_element is None):
            return -1

        if isinstance(left_element, int) and isinstance(right_element, int):
            if left_element < right_element:
                return 1
            elif left_element > right_element:
                return -1

        if isinstance(left_element, list) and isinstance(right_element, list):
            sub_answer = is_in_the_right_order_given_two_lists(left_element, right_element)
            if sub_answer == 0:
                continue
            else:
                return sub_answer

        if isinstance(left_element, int) and isinstance(right_element, list):
            sub_answer = is_in_the_right_order_given_two_lists([left_element], right_element)
            if sub_answer == 0:
                continue
            else:
                return sub_answer

        if isinstance(left_element, list) and isinstance(right_element, int):
            sub_answer = is_in_the_right_order_given_two_lists(left_element, [right_element])
            if sub_answer == 0:
                continue
            else:
                return sub_answer

    # Undecided return None
    return 0
