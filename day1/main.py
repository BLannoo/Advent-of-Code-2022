import assertpy


def test_silver():
    with open('input.txt') as file:
        data = file.read()
    assertpy.assert_that(
        calories_per_elf_sorted(data)[-1]
    ).is_equal_to(68775)


def test_gold():
    with open('input.txt') as file:
        data = file.read()
    assertpy.assert_that(
        sum(calories_per_elf_sorted(data)[-3:])
    ).is_equal_to(202585)


def calories_per_elf_sorted(data):
    calories_per_elf = [
        sum([
            int(snack)
            for snack in elf.split('\n')
        ])
        for elf in data.split('\n\n')
    ]
    return sorted(calories_per_elf)
