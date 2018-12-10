import os
import sys
import numpy
import copy


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
            nodes.append({
                'position': position,
                'movement': movement
            })
        for v in nodes:
            v['position'][0] += abs(min_x)
            v['position'][1] += abs(min_y)
        max_x = max_x + abs(min_x)
        max_y = max_y + abs(min_y)
        second = -1

        height = set([max_y])
        done = False
        while not done:
            current_height = max(height)
            height = set([])
            width = set([])
            _copy = copy.deepcopy(nodes)
            for v in nodes:
                movement = v.get('movement')
                v['position'][0] += movement[0]
                v['position'][1] += movement[1]
                if v.get('position')[1] > current_height:
                    done = True
                    break
                else:
                    height.add(v.get('position')[1])
                    width.add(v.get('position')[0])
            second += 1

        self.output('second:', second)
        useless_columns = None
        max_x = max([x.get('position')[0] for x in _copy])
        max_y = max([x.get('position')[1] for x in _copy])
        night_sky = numpy.zeros(shape=(max_y + 1, max_x + 1))

        for v in _copy:
            position = v.get('position')
            night_sky[position[1]][position[0]] = 1
        for i, column in enumerate(night_sky.T):
            if 1.0 in column and useless_columns is None:
                useless_columns = i
                break
        for o in night_sky:
            if 1.0 not in o:
                continue
            self.output(' '.join([str(x).replace('.0', '').replace('0', '.') for x in o[useless_columns:]]))


if __name__ == '__main__':
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
