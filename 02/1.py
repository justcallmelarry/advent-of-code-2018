import os


class AdevntOfCode:
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

    def run(self):
        two = 0
        three = 0
        for box in self.input_list:
            t2 = False
            t3 = False
            chars = ''.join(set(box))
            for char in chars:
                if box.count(char) == 2:
                    t2 = True
                if box.count(char) == 3:
                    t3 = True
            if t2:
                two += 1
            if t3:
                three += 1

        self.output(f'twos: {two}', f'threes: {three}', f'checksum: {two * three}')

    def output(self, *_output):
        self._results += [str(x) for x in _output]

    def results(self):
        print('\n'.join(self._results))


if __name__ == '__main__':
    AOC = AdevntOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
