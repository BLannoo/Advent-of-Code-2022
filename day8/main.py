from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import pytest
import assertpy

EXAMPLE = Path('example.txt').read_text()
INPUT = Path('input.txt').read_text()


def test_silver_example():
    assertpy.assert_that(solve_silver(EXAMPLE)).is_equal_to(21)


def test_silver():
    assertpy.assert_that(solve_silver(INPUT)).is_equal_to(1719)


def test_gold_example():
    assertpy.assert_that(solve_gold(EXAMPLE)).is_equal_to(8)


def test_gold():
    assertpy.assert_that(solve_gold(INPUT)).is_equal_to(590824)


@pytest.mark.parametrize(
    'x,y,visible',
    [
        (1, 1, True),
        (2, 1, True),
        (3, 1, False),
        (1, 2, True),
        (2, 2, False),
        (3, 2, True),
        (1, 3, False),
        (2, 3, True),
        (3, 3, False),
    ]
)
def test_is_visible(x: int, y: int, visible: bool):
    assertpy.assert_that(Forest(EXAMPLE).is_visible(x, y)).is_equal_to(visible)


def solve_silver(data: str) -> int:
    forest = Forest(data)
    visible_count = 2 * forest.height + 2 * forest.width - 4
    for x in range(1, forest.width - 1):
        for y in range(1, forest.height - 1):
            if forest.is_visible(x, y):
                visible_count += 1
    return visible_count


def solve_gold(data: str) -> int:
    highest_scenic_score = 0
    forest = Forest(data)
    for x in range(1, forest.width - 1):
        for y in range(1, forest.height - 1):
            scenic_score = forest.scenic_score(x, y)
            if scenic_score > highest_scenic_score:
                highest_scenic_score = scenic_score
    return highest_scenic_score


@dataclass(frozen=True)
class Forest:
    data: str

    def is_visible(self, x: int, y: int) -> bool:
        if max(self.trees_left(x, y)) < self.tree(x, y):
            return True
        if max(self.trees_right(x, y)) < self.tree(x, y):
            return True
        if max(self.trees_top(x, y)) < self.tree(x, y):
            return True
        if max(self.trees_bottom(x, y)) < self.tree(x, y):
            return True
        return False

    def scenic_score(self, x: int, y: int) -> int:
        tree_house_height = self.tree(x, y)
        visible_trees_left = 0
        for tree in self.trees_left(x, y):
            visible_trees_left += 1
            if tree >= tree_house_height:
                break
        visible_trees_right = 0
        for tree in self.trees_right(x, y):
            visible_trees_right += 1
            if tree >= tree_house_height:
                break
        visible_trees_top = 0
        for tree in self.trees_top(x, y):
            visible_trees_top += 1
            if tree >= tree_house_height:
                break
        visible_trees_bottom = 0
        for tree in self.trees_bottom(x, y):
            visible_trees_bottom += 1
            if tree >= tree_house_height:
                break
        total = visible_trees_left * visible_trees_right * visible_trees_top * visible_trees_bottom
        return total

    @property
    @lru_cache
    def width(self):
        return len(self.data.split('\n')[0])

    @property
    @lru_cache
    def height(self):
        return len(self.data.split('\n'))

    def tree(self, x: int, y: int) -> int:
        return int(self.__data_as_line()[y * self.width + x])

    @lru_cache
    def __data_as_line(self):
        return self.data.replace('\n', '')

    def trees_left(self, x: int, y: int) -> Iterable[int]:
        return reversed(self.__trees(y * self.width, y * self.width + x))

    def trees_right(self, x: int, y: int) -> Iterable[int]:
        return self.__trees(y * self.width + x + 1, (y + 1) * self.width)

    def trees_top(self, x: int, y: int) -> Iterable[int]:
        return reversed(self.__trees(x, y * self.width + x, self.width))

    def trees_bottom(self, x: int, y: int) -> Iterable[int]:
        return self.__trees((y + 1) * self.width + x, self.width * self.height, self.width)

    def __trees(self, start: int, stop: int, increment: int = 1) -> list[int]:
        return [
            int(tree)
            for tree in self.__data_as_line()[start:stop:increment]
        ]
