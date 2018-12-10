from collections import deque
import os
import sys


class AdventOfCode:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.input = os.path.join(self.filepath, 'input.txt')
        self._results = []
        self.input_list = []

    def load_input(self):
        if any([x in sys.argv for x in ('--test', '-t')]):
            self.input = os.path.join(self.filepath, 'sample.txt')
        if any([x in sys.argv for x in ('--all', '-a')]):
            self.input = os.path.join(self.filepath, 'all_samples.txt')
        with open(self.input, 'r') as input_file:
            for line in input_file.read().split('\n'):
                if line == '':
                    continue
                line = line.split(' ')
                self.input_list.append([int(line[0]), int(line[-2])])

    def output(self, *_output):
        self._results += [str(x) for x in _output]

    def results(self):
        print('\n'.join(self._results))

    def run(self):
        for game_id, game in enumerate(self.input_list):
            players = game[0]
            score = {}
            circle = deque([0])
            current_player = 1
            for marble in range(1, game[1] * 100 + 1):
                if marble % 23 == 0:
                    if current_player not in score:
                        score[current_player] = 0
                    score[current_player] += marble
                    circle.rotate(-7)
                    extra = circle.pop()
                    score[current_player] += extra
                else:
                    circle.rotate(2)
                    circle.append(marble)
                if current_player == players:
                    current_player = 1
                else:
                    current_player += 1

            winning_player = max(score, key=score.get)
            self.output(f'winner: elf #{winning_player}', f'winning score: {score.get(winning_player)}', ' ')


if __name__ == '__main__':
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
