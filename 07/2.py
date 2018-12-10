import os
import sys
import string
import time


class AdventOfCode:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.input = os.path.join(self.filepath, 'input.txt')
        self._results = []
        self.input_list = []
        self.alphabet_values = dict(zip(string.ascii_lowercase, [ord(c) % 32 for c in string.ascii_lowercase]))

    def load_input(self):
        if any([x in sys.argv for x in ('--test', '-t')]):
            self.input = os.path.join(self.filepath, 'sample.txt')
        with open(self.input, 'r') as input_file:
            for line in input_file.read().split('\n'):
                if line == '':
                    continue
                self.input_list.append(line)

    def output(self, *_output):
        self._results += [str(x) for x in _output]

    def results(self):
        print('\n'.join(self._results))

    def run(self):
        steps = set([])
        instructions = {}
        for instruction in self.input_list:
            instruction_list = instruction.split(' ')
            requirement = instruction_list[1]
            step = instruction_list[7]
            if step not in steps:
                steps.add(step)
            if requirement not in steps:
                steps.add(requirement)
            if step not in instructions:
                instructions[step] = {
                    'requirements': [],
                    'seconds': 60 + self.alphabet_values[step.lower()]
                }
                if '-t' in sys.argv:
                    instructions[step]['seconds'] -= 60
            if requirement not in instructions:
                instructions[requirement] = {
                    'requirements': [],
                    'seconds': 60 + self.alphabet_values[requirement.lower()]
                }
                if '-t' in sys.argv:
                    instructions[requirement]['seconds'] -= 60
            instructions[step]['requirements'].append(requirement)
        global_done = set([])
        second = 0
        workers = 5 if '-t' not in sys.argv else 2
        building = {}
        building_list = set([])
        progress = {}
        for i in range(workers):
            building[i] = None
        while len(steps):
            for k, v in dict(progress).items():
                target = instructions.get(k, {}).get('seconds')
                if not target:
                    target = 60 + self.alphabet_values[step.lower()]
                    if '-t' in sys.argv:
                        target -= 60
                if v == target:
                    global_done.add(k)
                    steps.remove(k)
                    progress.pop(k)
                    building_list.remove(k)
                    for worker, value in building.items():
                        if value == k:
                            building[worker] = None
                    for letter, x in instructions.items():
                        if k in x.get('requirements'):
                            instructions[letter]['requirements'].remove(k)
                else:
                    progress[k] += 1

            for step in list(sorted(steps)):
                if step in global_done:
                    continue
                dependencies = instructions.get(step, {}).get('requirements', [])
                if len(dependencies) == 0:
                    if step not in building_list:
                        for k, v in building.items():
                            if not v:
                                building[k] = step
                                building_list.add(step)
                                if step not in progress:
                                    progress[step] = 1
                                break
            if '-t' in sys.argv:
                time.sleep(0.2)
            if len(steps):
                second += 1
        self.output(second)


if __name__ == '__main__':
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
