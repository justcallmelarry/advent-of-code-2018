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
        _output = '\n'.join(self._results)
        print(_output)
        if '-d' in sys.argv:
            with open(os.path.join(self.filepath, f'results-{__file__}.txt'), 'w') as results_file:
                results_file.write(_output)
                results_file.write('\n')

    def run(self):
        def move_nodes(_list):
            return_list = []
            height = set([])
            width = set([])
            done = False
            for v in _list:
                pos_x = v[0] + v[2]
                pos_y = v[1] + v[3]
                if pos_y > self.current_height or pos_x > self.current_width:
                    done = True
                else:
                    width.add(pos_x)
                    height.add(pos_y)
                return_list.append([pos_x, pos_y, v[2], v[3]])
            return done, return_list, height, width

        nodes = []
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for node in self.input_list:
            node = node.replace('position=<', '').replace(' velocity=', '').replace('>', '').split('<')
            position = node[0].strip().split(',')
            position = [int(x) for x in position]
            movement = node[1].strip().split(',')
            movement = [int(x) for x in movement]
            min_x = min(min_x, position[0])
            max_x = max(max_x, position[0])
            min_y = min(min_y, position[1])
            max_y = max(max_y, position[1])
            nodes.append([position[0], position[1], movement[0], movement[1]])
        for v in nodes:
            v[0] += abs(min_x)
            v[1] += abs(min_y)
        max_x = max_x + abs(min_x)
        max_y = max_y + abs(min_y)
        second = -1

        height = set([max_y])
        width = set([max_x])
        done = False
        while not done:
            self.current_height = max(height)
            self.current_width = max(width)
            # _copy = copy.deepcopy(nodes)
            _copy = list(nodes)
            done, nodes, height, width = move_nodes(nodes)
            second += 1

        self.output('second:', second)
        useless_columns = None
        min_x = min([x[0] for x in _copy])
        max_x = max([x[0] for x in _copy])
        min_y = min([x[1] for x in _copy])
        max_y = max([x[1] for x in _copy])
        for v in _copy:
            v[0] -= min_x
            v[1] -= min_y
        max_x -= min_x
        max_y -= min_y
        night_sky = numpy.zeros(shape=(max_y + 1, max_x + 1))

        for v in _copy:
            night_sky[v[1]][v[0]] = 1
        for i, column in enumerate(night_sky.T):
            if 1.0 in column and useless_columns is None:
                useless_columns = i
                break
        for o in night_sky:
            if 1.0 not in o:
                continue
            self.output(' '.join([str(x).replace('.0', '').replace('0', ' ').replace('1', 'X') for x in o[useless_columns:]]))


if __name__ == '__main__':
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
