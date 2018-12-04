import os


class AdevntOfCode:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.input = os.path.join(self.filepath, 'input.txt')
        self._results = []
        self.input_list = []

        self.frequency_list = set([0])
        self.frequency = 0, False

    def load_input(self):
        with open(self.input, 'r') as input_file:
            for line in input_file.read().split('\n'):
                if line == '':
                    continue
                self.input_list.append(int(line.replace('+', '')))

    def run(self):
        while not self.frequency[1]:
            self.frequency = self.calc_freq(self.frequency)

        self.output(self.frequency[0])

    def output(self, *_output):
        self._results += [str(x) for x in _output]

    def results(self):
        print('\n'.join(self._results))

    def calc_freq(self, frequency):
        frequency = frequency[0]
        for adjustment in self.input_list:
            frequency += adjustment
            if int(frequency) in self.frequency_list:
                return frequency, True
            else:
                self.frequency_list.add(int(frequency))
        return frequency, False


if __name__ == "__main__":
    AOC = AdevntOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
