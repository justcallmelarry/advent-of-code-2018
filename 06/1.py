import os
import sys
import numpy


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
        outer_edges = set([])
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if table[y][x] != 0:
                    continue
                shortest_dist = None
                shortest_key = None
                for key, coord in coords.items():
                    dx = abs(coord[0] - x)
                    dy = abs(coord[1] - y)
                    manhattan_distance = abs(dx + dy)
                    if not shortest_dist or manhattan_distance < shortest_dist:
                        shortest_dist = manhattan_distance
                        shortest_key = key
                    elif shortest_dist == manhattan_distance:
                        shortest_key = 0
                table[y, x] = shortest_key
                if any([y == 1, y == max_y, x == 1, x == max_x]) and shortest_key not in outer_edges:
                    outer_edges.add(shortest_key)
        table_copy = numpy.array(list(table))
        max_area = 0
        max_key = None
        for x in outer_edges:
            table_copy[table_copy == x] = 0
        for x in coords.keys():
            if x not in outer_edges:
                area = len(table_copy[table_copy == x])
                if area > max_area:
                    max_area = area
                    max_key = x
        self.output(max_area, max_key)


if __name__ == '__main__':
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
