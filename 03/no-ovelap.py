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
        fabric_width = 0
        fabric_height = 0
        claims = {}
        for claim in self.input_list:
            claim = claim.replace(': ', ' @ ')
            claim = claim.split(' @ ')
            _id = claim[0].replace('#', '')
            coords = claim[1].split(',')
            size = claim[2].split('x')
            if _id not in claims:
                claims[_id] = {'coords': coords, 'size': size}
            height = int(coords[1]) + int(size[1])
            if height > fabric_height:
                fabric_height = height
            width = int(coords[0]) + int(size[0])
            if width > fabric_width:
                fabric_width = width

        self.fabric = []
        for _ in range(fabric_height + 1):
            self.fabric.append([0] * fabric_width)
        for k, v in claims.items():
            self.add_claim(v)

        for k, v in claims.items():
            correct = self.add_claim(v, second_round=True)
            if correct:
                self.output(k)

    def add_claim(self, claim, second_round=False):
        found_it = True
        for h in range(int(claim.get('coords')[1]), int(claim.get('coords')[1]) + int(claim.get('size')[1])):
            for w in range(int(claim.get('coords')[0]), int(claim.get('coords')[0]) + int(claim.get('size')[0])):
                if not second_round:
                    if self.fabric[h][w] == 0:
                        self.fabric[h][w] = 1
                    elif self.fabric[h][w] == 1:
                        self.fabric[h][w] = 2
                else:
                    if self.fabric[h][w] == 2:
                        found_it = False
        return found_it


if __name__ == "__main__":
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
