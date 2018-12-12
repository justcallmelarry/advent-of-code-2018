import os
import sys
from collections import defaultdict


class AdventOfCode:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.input = os.path.join(self.filepath, 'input.txt')
        self._results = []
        self.input_list = []

    def load_input(self):
        if any([x in sys.argv for x in ('--test', '-t')]):
            self.input = os.path.join(self.filepath, 'sample.txt')
        with open(self.input, 'r') as input_file:
            for line in input_file.read().split('\n'):
                if line == '':
                    continue
                self.input_list.append(line)
        self.initial_state = self.input_list.pop(0).replace('initial state: ', '')

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
        self.patterns = defaultdict(str)
        for x in self.input_list:
            pattern = x.split(' => ')
            self.patterns[pattern[0]] = pattern[1]
        state = None
        new_state = '#'
        old_state = '.'
        same_state = 0
        self.left_pots = 0
        generations = 0
        while same_state < 10:
            if not state:
                state = '....' + self.initial_state + '....'
                self.left_pots += 4
            else:
                old_state = state.strip('.')
                state = self.calc_gen(state)
            generations += 1
            new_state = state.strip('.')
            if old_state == new_state:
                same_state += 1

        offset = state.find('#') + 1
        offset = generations - offset + self.left_pots
        state = state.lstrip('.')
        offset = 50000000000 - offset
        ans = 0
        for i, x in enumerate(state):
            if x == '#':
                ans += i + offset
        self.output(ans)

    def calc_gen(self, _str):
        state = _str[0:2]
        for i, pot in enumerate(_str[2:-2], start=2):
            pattern = _str[i - 2: i + 3]
            growth = self.patterns.get(pattern, '.')
            state += growth
        if '#' in state[:4]:
            state = '....' + state
            self.left_pots += 4
        if '#' in state[-4:]:
            state += '....'
        return state


if __name__ == '__main__':
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
