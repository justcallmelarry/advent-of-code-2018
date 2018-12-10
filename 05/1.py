import os


class AdventOfCode:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.input = os.path.join(self.filepath, 'input.txt')
        self._results = []
        self.input_list = []

    def load_input(self):
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
        polymers = []
        for s in self.input_list[0]:
            polymers.append(s)
        found = True
        while found:
            polymers, found = self.remove_reactions(polymers)
        self.output(len(polymers))

    def remove_reactions(self, polymers):
        remove = set([])
        found = False
        for i in range(len(polymers)):
            if i in remove:
                continue
            if i == len(polymers) - 1:
                continue
            a = polymers[i]
            b = polymers[i + 1]
            if a.lower() == b.lower():
                if all([a.islower(), b.isupper()]) or all([a.isupper(), b.islower()]):
                    remove.add(i)
                    remove.add(i + 1)
                    found = True
        for i in sorted(remove, reverse=True):
            del polymers[i]
        return polymers, found


if __name__ == '__main__':
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
