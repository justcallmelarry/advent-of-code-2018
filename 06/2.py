import os
import sys
import numpy


class AdventOfCode:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.input = os.path.join(self.filepath, 'input.txt')
        self._results = []
        self.input_list = []
        self.target = 10000

    def load_input(self):
        if any([x in sys.argv for x in ('--test', '-t')]):
            self.target = 32
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
        max_x = 0
        max_y = 0
        coords = {}
        for i, _input in enumerate(self.input_list, start=1):
            x, y = _input.split(', ')
            x = int(x)
            y = int(y)
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            coords[i] = [x, y]
        table = numpy.zeros(shape=(max_y + 1, max_x + 1))
        for key, coord in coords.items():
            table[coord[1]][coord[0]] = key
        safe_area = 0
        safe_tiles = []
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                total_dist = 0
                for key, coord in coords.items():
                    dx = abs(coord[0] - x)
                    dy = abs(coord[1] - y)
                    manhattan_distance = abs(dx + dy)
                    total_dist += manhattan_distance
                    if total_dist > self.target:
                        break
                if total_dist < self.target:
                    safe_area += 1
                    safe_tiles.append([x, y, total_dist])
        # print(safe_tiles)
        self.output(safe_area)


if __name__ == "__main__":
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
