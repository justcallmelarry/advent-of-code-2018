import os
import sys


class Node:
    def __init__(self, name, parent=None, child_count=0, metadata_count=0):
        self.name = name
        self.metadata_count = metadata_count
        self.metadata = []
        self.parent = parent
        self.children = []
        self.child_count = child_count
        self.value = 0

        if parent:
            parent.children.append(self)

    def __repr__(self) -> str:
        return f'<Node {self.name} [{self.child_count}]>'

    def find_children_by_name(self, name):
        return [c for c in self.children if c.name == name]


class AdventOfCode:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.input = os.path.join(self.filepath, 'input.txt')
        self._results = []
        self.input_list = []
        self.answer = 0

    def load_input(self):
        if any([x in sys.argv for x in ('--test', '-t')]):
            self.input = os.path.join(self.filepath, 'sample.txt')
        with open(self.input, 'r') as input_file:
            for line in input_file.read().split(' '):
                if line == '':
                    continue
                self.input_list.append(int(line))

    def output(self, *_output):
        self._results += [str(x) for x in _output]

    def results(self):
        print('\n'.join(self._results))

    def run(self):
        self.nodes = 1
        copy_list = list(self.input_list)
        self.create_nodes(copy_list)
        # self.calc_answer(self.root)
        # self.output(self.answer)

    def calc_answer(self, node):
        for x in node.metadata:
            self.answer += x
        for child in node.children:
            self.calc_answer(child)

    def create_nodes(self, _list):
        def calculate_value(node):
            if node.child_count == 0:
                node.value = sum(node.metadata)
            else:
                for x in node.metadata:
                    try:
                        node.value += node.children[x - 1].value
                    except Exception:
                        pass

        def create_subchildren(_node, _sublist):
            children = _sublist.pop(0)
            metadata = _sublist.pop(0)
            node = Node(f'#{self.nodes}', child_count=children, metadata_count=metadata, parent=_node)
            self.nodes += 1
            for child in range(children):
                _sublist = create_subchildren(node, _sublist)
            for _ in range(metadata):
                node.metadata.append(_sublist.pop(0))
            calculate_value(node)
            print(node, 'child of', _node, 'value:', node.value)
            return _sublist

        children = _list.pop(0)
        metadata = _list.pop(0)
        self.root = Node(f'#{self.nodes}', child_count=children, metadata_count=metadata)
        print(self.root)
        self.nodes += 1
        for _ in range(children):
            _list = create_subchildren(self.root, _list)
        self.root.metadata = _list
        calculate_value(self.root)
        self.output(self.root.value)


if __name__ == '__main__':
    AOC = AdventOfCode()
    AOC.load_input()
    AOC.run()
    AOC.results()
