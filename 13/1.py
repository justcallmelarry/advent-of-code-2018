import os
import sys
from collections import deque


class AdventOfCode:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.input = os.path.join(self.filepath, 'input.txt')
        self._results = []
        self.input_list = []
        self.cart_info = {
            '<': ['-', 'w'],
            '>': ['-', 'e'],
            'v': ['|', 's'],
            '^': ['|', 'n']
        }
        self.direction_info = {
            'e': 1,
            'w': -1,
            'n': -1,
            's': 1
        }
        self.test = False

    def load_input(self):
        if any([x in sys.argv for x in ('--test', '-t')]):
            self.input = os.path.join(self.filepath, 'sample.txt')
            self.test = True
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
        cart_count = 0
        self.carts = []
        self.railway = []
        locations = deque()
        for s in self.input_list:
            self.railway.append(list(s))
        for y, y_content in enumerate(self.railway):
            for x, x_content in enumerate(y_content):
                if x_content in ('v', '^', '<', '>'):
                    cart = Cart(cart_count, x, y, self.cart_info.get(x_content)[1])
                    self.carts.append(cart)
                    cart_count += 1
                    self.railway[y][x] = self.cart_info.get(x_content)[0]
        for cart in sorted(self.carts, key=lambda x: (x.y, x.x)):
            locations.append((cart.x, cart.y))
        crashes = []
        ticks = 0
        while not crashes:
            for cart in sorted(self.carts, key=lambda x: (x.y, x.x)):
                locations.popleft()
                self.move_cart(cart)
                coords = (cart.x, cart.y)
                if coords not in locations:
                    locations.append(coords)
                else:
                    crashes.append(coords)
            ticks += 1
        self.output(ticks)
        self.output(crashes)

    def move_cart(self, _cart):
        if _cart.direction in ('e', 'w'):
            _cart.x += self.direction_info.get(_cart.direction)
        elif _cart.direction in ('n', 's'):
            _cart.y += self.direction_info.get(_cart.direction)
        next_step = self.railway[_cart.y][_cart.x]
        if next_step == '+':
            _cart.direction = _cart.turn_info.get((_cart.turn_sequence[(_cart.turns + 3) % 3])).get(_cart.direction)
            _cart.turns += 1
        elif next_step in ('\\', '/'):
            _cart.direction = _cart.turn_info.get(next_step).get(_cart.direction)

    def debug_print(self):
        _list = []
        for y in self.railway:
            _list.append([x for x in y])
        for c in self.carts:
            _list[c.y][c.x] = '#'
        for o in _list:
            print(''.join(o))
        print()


class Cart:
    def __init__(self, _id, x, y, direction):
        self._id = _id
        self.x = x
        self.y = y
        self.direction = direction
        self.turns = 0
        self.turn_sequence = ('left', 'straight', 'right')
        self.turn_info = {
            'left': {
                'e': 'n',
                'w': 's',
                'n': 'w',
                's': 'e'
            },
            'right': {
                'e': 's',
                'w': 'n',
                'n': 'e',
                's': 'w'
            },
            'straight': {
                'e': 'e',
                'w': 'w',
                'n': 'n',
                's': 's'
            },
            '\\': {
                'e': 's',
                'n': 'w',
                's': 'e',
                'w': 'n'
            },
            '/': {
                'e': 'n',
                'n': 'e',
                's': 'w',
                'w': 's'
            }
        }


if __name__ == '__main__':
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
