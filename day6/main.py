from collections import Counter
from pathlib import Path

import assertpy
import pytest


@pytest.mark.parametrize(
    'data,marker',
    [
        ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7),
        ('bvwbjplbgvbhsrlpgdmjqwftvncz', 5),
        ('nppdvjthqldpwncqszvftbrmjlhg', 6),
        ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10),
        ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11),
    ]
)
def test_silver_example(data: str, marker: int):
    assertpy.assert_that(solve(data, 4)).is_equal_to(marker)


def test_silver():
    data = Path('input.txt').read_text()
    assertpy.assert_that(solve(data, 4)).is_equal_to(1848)


@pytest.mark.parametrize(
    'data,marker',
    [
        ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 19),
        ('bvwbjplbgvbhsrlpgdmjqwftvncz', 23),
        ('nppdvjthqldpwncqszvftbrmjlhg', 23),
        ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 29),
        ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 26),
    ]
)
def test_gold_example(data: str, marker: int):
    assertpy.assert_that(solve(data, 14)).is_equal_to(marker)


def test_gold():
    data = Path('input.txt').read_text()
    assertpy.assert_that(solve(data, 14)).is_equal_to(2308)


def solve(data: str, size: int) -> int:
    for i in range(len(data) - size):
        marker = data[i:i + size]
        if Counter(marker).most_common()[0][1] == 1:
            return i + size
    return 0
