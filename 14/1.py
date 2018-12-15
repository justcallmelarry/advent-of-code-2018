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
        training_recipes = 157901
        target_recipes = 10
        total_recipes = training_recipes + target_recipes
        elves = []
        elf_count = 2
        for elf in range(elf_count):
            elves.append(Elf(elf, self.input_list[elf], elf))
        while len(self.input_list) < total_recipes:
            new_recipe = sum([x.recipe for x in elves])
            print(new_recipe)
            if new_recipe >= 10:
                self.input_list.append(int(new_recipe / 10 % 10))
                self.input_list.append(int(new_recipe % 10))
            else:
                self.input_list.append(new_recipe)
            for elf in elves:
                print(elf)
                elf.pos += elf.recipe + 1
                while elf.pos >= len(self.input_list):
                    elf.pos -= len(self.input_list)
                elf.recipe = self.input_list[elf.pos]
        self.output(''.join([str(x) for x in self.input_list[training_recipes:total_recipes]]))


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
