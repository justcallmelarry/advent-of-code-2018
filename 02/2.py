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
        correct_ids: list = []
        for _id in self.input_list:
            if _id in correct_ids:
                continue
            for compare_id in self.input_list:
                if _id == compare_id:
                    continue
                if compare_id in correct_ids:
                    continue
                faults = 0
                for one, two in zip(_id, compare_id):
                    if one != two:
                        faults += 1
                if faults > 1:
                    continue
                correct_ids.append(_id)
                correct_ids.append(compare_id)

        if len(correct_ids) != 2:
            self._results.appemd('incorrect amount of ids')
            return
        output = ''
        for one, two in zip(correct_ids[0], correct_ids[1]):
            if one == two:
                output += one

        self.output(output)

    def output(self, *_output):
        self._results += [str(x) for x in _output]

    def results(self):
        print('\n'.join(self._results))


if __name__ == '__main__':
    AOC = AdevntOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
