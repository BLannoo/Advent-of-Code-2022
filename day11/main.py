import math
import re
from dataclasses import dataclass, field
from typing import Callable


def solve_silver(data: str, rounds: int = 20) -> int:
    monkeys = parse(data)
    for _ in range(rounds):
        execute_round(monkeys)
    return monkey_business(monkeys)


def solve_gold(data: str, rounds: int = 10_000) -> int:
    monkeys = parse(data)
    worry_modulo = calculate_worry_modulo(monkeys)
    for _ in range(rounds):
        execute_round(monkeys, worry_modulo, with_relief=False)
    return monkey_business(monkeys)


MONKEY_REGEX = r'''
Monkey (?P<id>\d+):
  Starting items: (?P<items>(?:\d+,? ?)+)
  Operation: new = (?P<operation>[\w\d]+ [\*\+-/] [\w\d]+)
  Test: divisible by (?P<test_value>\d+)
    If true: throw to monkey (?P<true_monkey>\d+)
    If false: throw to monkey (?P<false_monkey>\d+)
'''.strip('\n')


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: Callable[[int], int] = field(compare=False)
    test_value: int
    true_monkey: int
    false_monkey: int
    inspected: int = 0

    @classmethod
    def parse(cls, monkey_description: str) -> 'Monkey':
        match = re.match(
            MONKEY_REGEX, monkey_description
        )
        items = [
            int(item)
            for item in match.group('items').split(', ')
        ]
        operation_body = match.group('operation')
        d = {}
        exec(f'def operation(old): return {operation_body}', d)
        return Monkey(
            id=int(match.group('id')),
            items=items,
            operation=d['operation'],
            test_value=int(match.group('test_value')),
            true_monkey=int(match.group('true_monkey')),
            false_monkey=int(match.group('false_monkey')),
        )

    def has_items(self) -> bool:
        return len(self.items) > 0

    def process_next_item(self, worry_modulo: int = None, with_relief: bool = True) -> tuple[int, int]:
        old_worry_level = self.items.pop(0)
        self.inspected += 1
        new_worry_level = self.operation(old_worry_level)
        if with_relief:
            new_worry_level //= 3
        if worry_modulo:
            new_worry_level %= worry_modulo
        if new_worry_level % self.test_value == 0:
            return self.true_monkey, new_worry_level
        return self.false_monkey, new_worry_level

    def receive_item(self, worry_level: int) -> None:
        self.items.append(worry_level)

    def summarize(self) -> str:
        items = ', '.join([str(item) for item in self.items])
        return f'Monkey {self.id}: {items}'


def parse(data: str) -> list[Monkey]:
    return [
        Monkey.parse(monkey_description)
        for monkey_description in data.split('\n\n')
    ]


def calculate_worry_modulo(monkeys):
    return math.prod(
        monkey.test_value
        for monkey in monkeys
    )


def execute_round(monkeys, worry_modulo: int = None, with_relief: bool = True):
    for monkey in monkeys:
        while monkey.has_items():
            (recipient_monkey, worry_level) = monkey.process_next_item(worry_modulo, with_relief)
            monkeys[recipient_monkey].receive_item(worry_level)


def monkey_business(monkeys: list[Monkey]) -> int:
    inspections = sorted([
        monkey.inspected
        for monkey in monkeys
    ])
    return inspections[-1] * inspections[-2]
