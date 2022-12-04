from pathlib import Path
from typing import Dict

import assertpy


def solve(data_file_path: Path, lookup_table: Dict[str, int]) -> int:
    data = data_file_path.read_text()
    return sum([
        lookup_table[round_description.strip()]
        for round_description in data.split('\n')
    ])


SILVER_TABLE = {
    "A X": 4,
    "B X": 1,
    "C X": 7,
    "A Y": 8,
    "B Y": 5,
    "C Y": 2,
    "A Z": 3,
    "B Z": 9,
    "C Z": 6,
}

GOLD_TABLE = {
    "A X": 3,
    "B X": 1,
    "C X": 2,
    "A Y": 4,
    "B Y": 5,
    "C Y": 6,
    "A Z": 8,
    "B Z": 9,
    "C Z": 7,
}

EXAMPLE = '''
A Y
B X
C Z
'''.strip()


def test_silver_example():
    assertpy.assert_that(solve(Path("example.txt"), SILVER_TABLE)).is_equal_to(15)


def test_silver():
    assertpy.assert_that(solve(Path('input.txt'), SILVER_TABLE)).is_equal_to(15691)


def test_gold_example():
    assertpy.assert_that(solve(Path('example.txt'), GOLD_TABLE)).is_equal_to(12)


def test_gold():
    assertpy.assert_that(solve(Path('input.txt'), GOLD_TABLE)).is_equal_to(12989)
