import os
import sys
import numpy


class AdventOfCode:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.input = 5177 if '-t' not in sys.argv else 18
        self._results = []

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
        grid = numpy.zeros(shape=(300, 300), dtype=numpy.int)
        for y in range(300):
            for x in range(300):
                grid[y][x] = self.calc_value(x + 1, y + 1)

        best_coords = []
        best_sum = 0
        square_size = 0
        for y in range(300):
            for x in range(300):
                for chunksize in range(1, 301 - max(x, y)):
                    subgrid = (grid[y: y + chunksize, x: x + chunksize])
                    if subgrid.sum() > best_sum:
                        best_coords = [x + 1, y + 1]
                        best_sum = subgrid.sum()
                        square_size = chunksize
        self.output(f'{best_coords[0]},{best_coords[1]},{square_size} - {best_sum}')

    def calc_value(self, x, y):
        rackid = x + 10
        value = rackid * y
        value += self.input
        value *= rackid
        if value > 100:
            return int(value / 100) % 10 - 5
        else:
            return -5


if __name__ == '__main__':
    AOC = AdventOfCode()
    AOC.run()
    AOC.results()
