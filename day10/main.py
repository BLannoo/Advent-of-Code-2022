from pathlib import Path

import assertpy
import pytest

EXAMPLE = Path('example.txt').read_text()
INPUT = Path('input.txt').read_text()


def test_silver_example():
    assertpy.assert_that(solve(EXAMPLE)).is_equal_to(13140)


def test_silver():
    assertpy.assert_that(solve(INPUT)).is_equal_to(12560)


EXAMPLE_OUTPUT = '''
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
'''


def test_gold_example():
    assertpy.assert_that(solve_gold(EXAMPLE)).is_equal_to(EXAMPLE_OUTPUT)


OUTPUT = '''
###..#....###...##..####.###...##..#....
#..#.#....#..#.#..#.#....#..#.#..#.#....
#..#.#....#..#.#..#.###..###..#....#....
###..#....###..####.#....#..#.#....#....
#....#....#....#..#.#....#..#.#..#.#....
#....####.#....#..#.#....###...##..####.
'''


def test_gold():
    assertpy.assert_that(solve_gold(INPUT)).is_equal_to(OUTPUT)


@pytest.mark.parametrize(
    'cycle,value',
    [
        (20, 21),  # During the 20th cycle, register X has the value 21
        (60, 19),  # During the 60th cycle, register X has the value 19
        (100, 18),  # During the 100th cycle, register X has the value 18
        (140, 21),  # During the 140th cycle, register X has the value 21
        (180, 16),  # During the 180th cycle, register X has the value 16
        (220, 18),  # During the 220th cycle, register X has the value 18
    ]
)
def test_run_instructions(cycle: int, value: int):
    register_history = run_instructions(EXAMPLE)
    assertpy.assert_that(register_history[cycle - 1]).is_equal_to(value)


def solve(data: str) -> int:
    register_history = run_instructions(data)
    return sum(
        register_history[selected_cycle - 1] * selected_cycle
        for selected_cycle in range(20, 220 + 1, 40)
    )


def solve_gold(data: str, screen_width: int = 40, screen_height: int = 6) -> str:
    register_history = run_instructions(data)
    display = '\n'
    for y in range(screen_height):
        for x in range(screen_width):
            index = y * screen_width + x
            if abs(register_history[index] - x) <= 1:
                display += '#'
            else:
                display += '.'
        display += '\n'
    return display


def run_instructions(data):
    register_history = [1]
    for instruction in data.split('\n'):
        register_history.append(register_history[-1])
        if instruction == 'noop':
            continue
        elif instruction[:4] == 'addx':
            value = int(instruction[5:])
            register_history.append(register_history[-1] + value)
        else:
            raise ValueError(f'Received invalid {instruction=}')
    return register_history
