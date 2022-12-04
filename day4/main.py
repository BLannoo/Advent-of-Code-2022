import re
from pathlib import Path
from typing import Callable

import assertpy
import pytest

ELF_PAIR_REGEX = r'(?P<start_first_elf>\d+)-(?P<end_first_elf>\d+),(?P<start_second_elf>\d+)-(?P<end_second_elf>\d+)'


def test_silver_example():
    assertpy.assert_that(solve(Path('example.txt'), fully_contains)).is_equal_to(2)


def test_silver():
    assertpy.assert_that(solve(Path('input.txt'), fully_contains)).is_equal_to(550)


def test_gold_example():
    assertpy.assert_that(solve(Path('example.txt'), overlaps)).is_equal_to(4)


def test_gold():
    assertpy.assert_that(solve(Path('input.txt'), overlaps)).is_equal_to(931)


@pytest.mark.parametrize(
    'elf_pair,expected',
    [
        ('2-4,6-8', False),
        ('2-3,4-5', False),
        ('5-7,7-9', False),
        ('2-8,3-7', True),
        ('6-6,4-6', True),
        ('2-6,4-8', False),
    ]
)
def test_fully_contains(elf_pair: str, expected: bool):
    assertpy.assert_that(fully_contains(elf_pair)).is_equal_to(expected)


@pytest.mark.parametrize(
    'elf_pair,expected',
    [
        ('2-4,6-8', False),
        ('2-3,4-5', False),
        ('5-7,7-9', True),
        ('2-8,3-7', True),
        ('6-6,4-6', True),
        ('2-6,4-8', True),
    ]
)
def test_overlaps(elf_pair: str, expected: bool):
    assertpy.assert_that(overlaps(elf_pair)).is_equal_to(expected)


def solve(file: Path, rule: Callable[[str], bool]) -> int:
    data = file.read_text()
    return sum(
        rule(elf_pair)
        for elf_pair in data.split('\n')
    )


def fully_contains(elf_pair: str) -> bool:
    match = re.match(pattern=ELF_PAIR_REGEX, string=elf_pair)
    if (
        int(match.group('start_first_elf'))
        <= int(match.group('start_second_elf'))
        <= int(match.group('end_second_elf'))
        <= int(match.group('end_first_elf'))
    ):
        return True

    if (
        int(match.group('start_second_elf'))
        <= int(match.group('start_first_elf'))
        <= int(match.group('end_first_elf'))
        <= int(match.group('end_second_elf'))
    ):
        return True
    return False


def overlaps(elf_pair: str) -> bool:
    match = re.match(pattern=ELF_PAIR_REGEX, string=elf_pair)
    if (
        int(match.group('start_second_elf'))
        <= int(match.group('start_first_elf'))
        <= int(match.group('end_second_elf'))
    ):
        return True
    if (
        int(match.group('start_second_elf'))
        <= int(match.group('end_first_elf'))
        <= int(match.group('end_second_elf'))
    ):
        return True
    if (
        int(match.group('start_first_elf'))
        <= int(match.group('end_second_elf'))
        <= int(match.group('end_first_elf'))
    ):
        return True
    return False
