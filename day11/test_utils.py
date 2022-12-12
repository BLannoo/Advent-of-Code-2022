from day11.main import Monkey


def monkeys_test_builder():
    return [
        Monkey(
            id=0,
            items=[79, 98],
            operation=lambda old: old * 19,
            test_value=23,
            true_monkey=2,
            false_monkey=3,
        ),
        Monkey(
            id=1,
            items=[54, 65, 75, 74],
            operation=lambda old: old + 6,
            test_value=19,
            true_monkey=2,
            false_monkey=0,
        ),
        Monkey(
            id=2,
            items=[79, 60, 97],
            operation=lambda old: old * old,
            test_value=13,
            true_monkey=1,
            false_monkey=3,
        ),
        Monkey(
            id=3,
            items=[74],
            operation=lambda old: old + 3,
            test_value=17,
            true_monkey=0,
            false_monkey=1,
        ),
    ]


def monkeys_printer(monkeys: list[Monkey]) -> str:
    return '\n'.join(
        monkey.summarize()
        for monkey in monkeys
    ).strip('\n ')


def inspections_printer(monkeys: list[Monkey]) -> str:
    return '\n'.join(
        f'Monkey {monkey.id} inspected items {monkey.inspected} times.'
        for monkey in monkeys
    )
