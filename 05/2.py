import os


class AdventOfCode:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.input = os.path.join(self.filepath, 'results.txt')
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
        chars = []
        test_input = self.input_list[0].lower()
        for s in self.input_list[0]:
            polymers.append(s)
        for s in test_input:
            chars.append(s)
        chars = set(chars)
        length = None
        best_char = None
        done = 0
        total = len(chars)
        for char in chars:
            test_polymers = [x for x in polymers if x not in (char.lower(), char.upper())]
            found = True
            while found:
                test_polymers, found = self.remove_reactions(test_polymers)
            print(char, len(test_polymers))
            if not length or len(test_polymers) < length:
                length = len(test_polymers)
                best_char = char
            done += 1
            print(f'{done} out of {total} done')
        self.output(best_char)
        self.output(length)

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
