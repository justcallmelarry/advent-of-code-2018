import os
import sys


class AdventOfCode:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.input = os.path.join(self.filepath, 'input.txt')
        self._results = []
        self.input_list = [3, 7]

    def output(self, *_output):
        self._results += [str(x) for x in _output]

    def results(self):
        _output = '\n'.join(self._results)
        print(_output)
        if '-d' in sys.argv:
            with open(os.path.join(self.filepath, f'results-{__file__}.txt'), 'w') as results_file:
                results_file.write(_output)
                results_file.write('\n')

    def run(self):
        self.checks = set()
        found = False
        seq = (1, 5, 7, 9, 0, 1) if '-t' not in sys.argv else (5, 1, 5, 8, 9)
        self.seq_len = len(seq)
        elves = []
        elf_count = 2
        for elf in range(elf_count):
            elves.append(Elf(elf, self.input_list[elf], elf))
        while not found:
            new_recipe = sum([x.recipe for x in elves])
            if new_recipe >= 10:
                self.input_list.append(int(new_recipe / 10 % 10))
                self.add_check()
                self.input_list.append(int(new_recipe % 10))
                self.add_check()
            else:
                self.input_list.append(new_recipe)
                self.add_check()
            if seq in self.checks:
                found = True
            for elf in elves:
                elf.pos += elf.recipe + 1
                while elf.pos >= len(self.input_list):
                    elf.pos -= len(self.input_list)
                elf.recipe = self.input_list[elf.pos]
        input_str = ''.join([str(x) for x in self.input_list])
        ans = input_str.split(''.join(str(x) for x in seq))
        self.output(len(ans[0]))

    def add_check(self):
        if len(self.input_list) > self.seq_len:
            self.checks.add(tuple(self.input_list[self.seq_len * -1:]))


class Elf:
    def __init__(self, _id, recipe, pos):
        self._id = _id
        self.recipe = recipe
        self.pos = pos

    def __repr__(self):
        return f'Elf #{self._id} at {self.pos} creating {self.recipe}'


if __name__ == '__main__':
    AOC = AdventOfCode()
    AOC.run()
    AOC.results()
