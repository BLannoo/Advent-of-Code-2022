from pathlib import Path
from typing import Tuple

import assertpy
import pytest as pytest


def test_silver_example():
    assertpy.assert_that(
        solve_silver(Path('example.txt'))
    ).is_equal_to(157)


def test_silver():
    assertpy.assert_that(
        solve_silver(Path('input.txt'))
    ).is_equal_to(8493)


def test_gold_example():
    assertpy.assert_that(
        solve_gold(Path('example.txt'))
    ).is_equal_to(70)


def test_gold():
    assertpy.assert_that(
        solve_gold(Path('input.txt'))
    ).is_equal_to(2552)


@pytest.mark.parametrize(
    'rucksack,error_item',
    [
        # From assignment
        ('vJrwpWtwJgWrhcsFMMfFFhFp', 'p'),
        ('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL', 'L'),
        ('PmmdzqPrVvPwwTWBwg', 'P'),
        ('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn', 'v'),
        ('ttgJtRGJQctTZtZT', 't'),
        ('CrZsJsPPZsGzwwsLwLmpwMDw', 's'),

        # Check split is happening in the middle
        ('abbc', 'b')
    ]
)
def test_find_error_item(rucksack: str, error_item: str):
    assertpy.assert_that(
        find_error_item(rucksack)
    ).is_equal_to(error_item)


@pytest.mark.parametrize(
    'error_item,priority',
    [
        ('p', 16),
        ('L', 38),
        ('P', 42),
        ('v', 22),
        ('t', 20),
        ('s', 19),
    ]
)
def test_determine_priority(error_item: str, priority: int):
    assertpy.assert_that(
        determine_priority(error_item)
    ).is_equal_to(priority)


@pytest.mark.parametrize(
    'group,badge',
    [
        (
            (
                'vJrwpWtwJgWrhcsFMMfFFhFp',
                'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
                'PmmdzqPrVvPwwTWBwg',
            ),
            'r'
        ),
        (
            (
                'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
                'ttgJtRGJQctTZtZT',
                'CrZsJsPPZsGzwwsLwLmpwMDw',
            ),
            'Z'
        )
    ]
)
def test_determine_badge(group: Tuple[str, str, str], badge: str):
    assertpy.assert_that(
        determine_badge(group)
    ).is_equal_to(badge)


def solve_silver(file: Path) -> int:
    data = file.read_text()
    rucksacks = data.split('\n')
    error_items = [
        find_error_item(rucksack)
        for rucksack in rucksacks
    ]
    priorities = [
        determine_priority(error_item)
        for error_item in error_items
    ]

    return sum(priorities)


def solve_gold(file: Path) -> int:
    data = file.read_text()
    rucksacks = data.split('\n')
    assert len(rucksacks) / 3 == len(rucksacks) // 3
    elf_groups = [
        (rucksacks[3 * i], rucksacks[3 * i + 1], rucksacks[3 * i + 2])
        for i in range(len(rucksacks) // 3)
    ]
    badge_items = [
        determine_badge(elf_group)
        for elf_group in elf_groups
    ]
    priorities = [
        determine_priority(badge_item)
        for badge_item in badge_items
    ]
    return sum(priorities)


def determine_badge(elf_group: Tuple[str, str, str]) -> str:
    common = set(elf_group[0]).intersection(set(elf_group[1])).intersection(set(elf_group[2]))
    assert len(common) == 1
    return common.pop()


def find_error_item(rucksack: str) -> str:
    len_rucksack = len(rucksack)
    assert len_rucksack / 2 == len_rucksack // 2
    first_compartment = rucksack[:len_rucksack // 2]
    second_compartment = rucksack[len_rucksack // 2:]
    overlapping_items = set(first_compartment).intersection(set(second_compartment))
    assert len(overlapping_items) == 1
    return overlapping_items.pop()


def determine_priority(error_item: str) -> int:
    if error_item.islower():
        return ord(error_item) - ord('a') + 1
    return ord(error_item) - ord('A') + 27
