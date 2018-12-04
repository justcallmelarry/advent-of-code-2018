import os
import numpy


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
        self.schedule = {}
        for schedule in sorted(self.input_list):
            data = schedule.split('] ')
            date_data = data[0].replace('[', '').split(' ')
            date = date_data[0]
            time_data = date_data[1]
            hour, minute = time_data.split(':')
            event = data[1]
            if event.startswith('Guard #'):
                guard = event.split(' ')[1].replace('#', '')
                if guard not in self.schedule:
                    self.schedule[guard] = {}
            if event == 'falls asleep':
                if date not in self.schedule[guard]:
                    self.schedule[guard][date] = []
                self.schedule[guard][date].append(f's{minute}')
            if event == 'wakes up':
                self.schedule[guard][date].append(f'w{minute}')

        for guard, date_data in self.schedule.items():
            self.schedule[guard]['wake_matrix'] = []
            for date, time_data in date_data.items():
                if date == 'wake_matrix':
                    continue
                self.schedule[guard]['wake_matrix'].append([0] * 60)
                self.create_schedule(
                    guard,
                    self.schedule[guard]['wake_matrix'][-1],
                    time_data
                )
        sleepy_guard = None
        sleepy_minute = 0
        sleepy_minute_value = 0
        for guard in self.schedule:
            matrix = numpy.matrix(self.schedule.get(guard).get('wake_matrix'))
            sums = matrix.sum(axis=0)
            sums = sums.tolist()
            if not sums[0]:
                continue
            minute_value = max(sums[0])
            minute = sums[0].index(minute_value)
            if minute_value > sleepy_minute_value:
                sleepy_guard = guard
                sleepy_minute = minute
                sleepy_minute_value = minute_value
        self.output(f'guard: {sleepy_guard}', f'minute: {sleepy_minute}', f'answer: {int(sleepy_guard) * int(sleepy_minute)}')

    def create_schedule(self, guard, schedule, data):
        while len(data) > 0:
            s = int(data.pop(0).replace('s', ''))
            w = int(data.pop(0).replace('w', ''))
            for x in range(s, w):
                schedule[x] = 1


if __name__ == "__main__":
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
