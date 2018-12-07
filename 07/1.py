import os
import sys


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
                instructions[step] = []
            instructions[step].append(requirement)

        answer = ''
        global_done = set([])
        while len(steps):
            done = set([])
            for step in list(sorted(steps)):
                if step in global_done:
                    continue
                dependencies = instructions.get(step, [])
                if len(dependencies) == 0:
                    done.add(step)
            im_stupid = sorted(done)[0]
            answer += im_stupid
            global_done.add(im_stupid)
            steps.remove(im_stupid)
            for v in instructions.values():
                if im_stupid in v:
                    v.remove(im_stupid)
        self.output(answer)


if __name__ == "__main__":
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
