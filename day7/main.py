from dataclasses import dataclass
from pathlib import Path
from typing import List

import assertpy


def test_silver_example():
    assertpy.assert_that(solve_silver(Path('example.txt'))).is_equal_to(95437)


def test_silver():
    assertpy.assert_that(solve_silver(Path('input.txt'))).is_equal_to(1232307)


def test_gold_example():
    assertpy.assert_that(solve_gold(Path('example.txt'))).is_equal_to(24933642)


def test_gold():
    assertpy.assert_that(solve_gold(Path('input.txt'))).is_equal_to(7268994)


@dataclass
class File:
    name: str
    size: int


def solve_silver(file: Path) -> int:
    root_folder = parse(file)
    all_folders = root_folder.get_all_folders()
    return sum(
        folder.size()
        for folder in all_folders
        if folder.size() <= 100_000
    )


def solve_gold(file: Path) -> int:
    available_space = 70_000_000
    needed_space = 30_000_000
    root_folder = parse(file)
    used_space = root_folder.size()
    unused_space = available_space - used_space
    to_free_space = needed_space - unused_space
    return min(
        folder.size()
        for folder in root_folder.get_all_folders()
        if folder.size() > to_free_space
    )


class Folder:
    def __init__(self, folder_name: str, parent_folder: 'Folder' = None):
        self.folder_name = folder_name
        self.parent_folder = parent_folder
        self.sub_folders: List['Folder'] = []
        self.files: List[File] = []

    def execute(self, command: str) -> 'Folder':
        if command[:2] == 'cd':
            return self.cd(command[3:])
        elif command[:2] == 'ls':
            lines = command.split('\n')
            self.ls(lines[1:])
            return self
        else:
            raise ValueError(f'Unknown command: {command}')

    def cd(self, folder_name: str) -> 'Folder':
        if folder_name == '..':
            return self.parent_folder
        if folder_name == '/':
            return self.root()
        for sub_folder in self.sub_folders:
            if sub_folder.folder_name == folder_name:
                return sub_folder
        new_folder = Folder(folder_name, self)
        self.sub_folders.append(new_folder)
        return new_folder

    def render(self, depth=0) -> str:
        representation = '  ' * depth + f'- {self.folder_name} (dir)\n'
        for sub_folder in self.sub_folders:
            representation += sub_folder.render(depth + 1)
        for file in self.files:
            representation += '  ' * depth + f'  - {file.name} (file, size={file.size})\n'
        return representation

    def ls(self, lines: List[str]):
        for line in lines:
            parts = line.split(' ')
            assert len(parts) == 2
            size = parts[0]
            name = parts[1]
            if size == 'dir':
                found = False
                for sub_folder in self.sub_folders:
                    if sub_folder.folder_name == name:
                        found = True
                if not found:
                    self.sub_folders.append(Folder(name, self))
            else:
                self.files.append(File(name, int(size)))

    def root(self):
        if self.parent_folder:
            return self.parent_folder.root()
        return self

    def get_all_folders(self) -> List['Folder']:
        all_folders = [
            folder
            for sub_folder in self.sub_folders
            for folder in sub_folder.get_all_folders()
        ]
        all_folders.append(self)
        return all_folders

    def size(self) -> int:
        return sum(
            sub_folder.size()
            for sub_folder in self.sub_folders
        ) + sum(
            file.size
            for file in self.files
        )


def parse(file):
    data = file.read_text()
    commands = data[2:].split('\n$ ')
    root_folder = Folder('/')
    current_folder = root_folder
    for command in commands:
        current_folder = current_folder.execute(command)
    return root_folder
