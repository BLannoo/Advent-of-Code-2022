import re
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, List, Callable

import assertpy


@dataclass
class Stack:
    crates: List[str]


EXAMPLE_STACKS_STRING = '''
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3
'''.strip('\n')

EXAMPLE_STACKS = [
    Stack(['N', 'Z']),
    Stack(['D', 'C', 'M']),
    Stack(['P']),
]


@dataclass(frozen=True)
class Move:
    _quantity: int
    _from: int
    _to: int


EXAMPLE_MOVES = [
    Move(_quantity=1, _from=2, _to=1),
    Move(_quantity=3, _from=1, _to=3),
    Move(_quantity=2, _from=2, _to=1),
    Move(_quantity=1, _from=1, _to=2),
]


def test_silver_example():
    assertpy.assert_that(solve(Path('example.txt'), execute_silver)).is_equal_to('CMZ')


def test_silver():
    assertpy.assert_that(solve(Path('input.txt'), execute_silver)).is_equal_to('VJSFHWGFT')


def test_gold_example():
    assertpy.assert_that(solve(Path('example.txt'), execute_gold)).is_equal_to('MCD')


def test_gold():
    assertpy.assert_that(solve(Path('input.txt'), execute_gold)).is_equal_to('LCTQFBVZV')


def test_parse_input():
    assertpy.assert_that(parse_input(Path('example.txt'))).is_equal_to(
        (EXAMPLE_STACKS, EXAMPLE_MOVES)
    )


def test_parse_stacks():
    assertpy.assert_that(parse_stacks(EXAMPLE_STACKS_STRING)).is_equal_to(EXAMPLE_STACKS)


def test_parse_move():
    assertpy.assert_that(parse_move('move 1 from 2 to 1')).is_equal_to(Move(_quantity=1, _from=2, _to=1))


def solve(file: Path, move_executor: Callable[[Move, List[Stack]], List[Stack]]) -> str:
    (stacks, moves) = parse_input(file)

    for move in moves:
        stacks = move_executor(move, stacks)

    return ''.join(
        stack.crates[0]
        for stack in stacks
    )


def execute_silver(move: Move, stacks: List[Stack]) -> List[Stack]:
    for _ in range(move._quantity):
        box = stacks[move._from - 1].crates.pop(0)
        stacks[move._to - 1].crates.insert(0, box)
    return stacks


def execute_gold(move: Move, stacks: List[Stack]) -> List[Stack]:
    boxes_to_move = stacks[move._from - 1].crates[:move._quantity]
    stacks[move._from - 1].crates = stacks[move._from - 1].crates[move._quantity:]
    stacks[move._to - 1].crates = boxes_to_move + stacks[move._to - 1].crates
    return stacks


def parse_input(file: Path) -> Tuple[List[Stack], List[Move]]:
    data = file.read_text()
    (stacks, moves) = data.split('\n\n')
    moves = [
        parse_move(move_line)
        for move_line in moves.split('\n')
    ]
    return parse_stacks(stacks), moves


def parse_stacks(stacks_description: str) -> List[Stack]:
    stack_lines = stacks_description.split('\n')
    stack_number = int(stack_lines[-1][-1])
    stacks = [
        []
        for _ in range(stack_number)
    ]
    for stack_line in stack_lines[:-1]:
        for i, letter in enumerate(stack_line[1::4]):
            if letter != ' ':
                stacks[i].append(letter)
    return [
        Stack(stack)
        for stack in stacks
    ]


def parse_move(move: str) -> Move:
    match = re.match(
        r'move (?P<_quantity>\d+) from (?P<_from>\d+) to (?P<_to>\d+)',
        move,
    )
    return Move(
        _quantity=int(match.group('_quantity')),
        _from=int(match.group('_from')),
        _to=int(match.group('_to')),
    )
