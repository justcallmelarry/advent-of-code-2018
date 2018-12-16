import sys
import collections


class Unit:
    hp = 200
    ap = 3
    dead = False

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{self._name} #{self.id} - {self.hp}'


class Goblin(Unit):
    _type = 'goblin'
    _name = 'G'


class Elf(Unit):
    _type = 'elf'
    _name = 'E'


def bfs(grid, start, target):
    grid[target[1]][target[0]] = '*'
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == '*':
            grid[target[1]][target[0]] = '.'
            return path
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] in ('.', '*') and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
    grid[target[1]][target[0]] = '.'


def move(battleground, unit, path):
    battleground[unit.y][unit.x] = '.'
    unit.x, unit.y = path[1]
    battleground[unit.y][unit.x] = unit._name


def kill_unit(unit, _list, units, battleground):
    unit.dead = True
    battleground[unit.y][unit.x] = '.'

    remove_from_list = None
    for i, x in enumerate(_list):
        if x.id == unit.id:
            remove_from_list = i
    if remove_from_list is not None:
        _list.pop(remove_from_list)

    remove_from_units = None
    for i, x in enumerate(units):
        if x.id == unit.id:
            remove_from_units = i
    if remove_from_units is not None:
        units.pop(remove_from_units)


def distance(battleground, unit, enemy):
    possible_coords = [
        (enemy.x - 1, enemy.y),
        (enemy.x + 1, enemy.y),
        (enemy.x, enemy.y + 1),
        (enemy.x, enemy.y - 1)
    ]
    shortest_path = None
    for coords in possible_coords:
        if battleground[coords[1]][coords[0]] != '.':
            continue
        path = bfs(battleground, (unit.x, unit.y), coords)
        if not path:
            continue
        elif not shortest_path or len(path) < len(shortest_path):
            shortest_path = path
        elif len(path) == len(shortest_path):
            if path[1][1] < shortest_path[1][1]:
                shortest_path = path
            elif path[1][0] == shortest_path[1][0] and path[1][0] < shortest_path[1][0]:
                shortest_path = path
    return shortest_path


def print_battleground(battleground, units):
    bgu = {}
    for unit in units:
        if unit.y not in bgu:
            bgu[unit.y] = []
        bgu[unit.y].append(unit)
    for y, o in enumerate(battleground):
        print(''.join(o), ' ' * 5, sorted(bgu.get(y, []), key=lambda x: x.x))
    print()


def main():
    units = []
    elves = []
    goblins = []
    battleground = []
    unit_id = 0
    for y, content in enumerate(_input):
        row = []
        for x, content in enumerate(content):
            if content == 'G':
                g = Goblin(unit_id, x, y)
                goblins.append(g)
                units.append(g)
                unit_id += 1
            elif content == 'E':
                e = Elf(unit_id, x, y)
                elves.append(e)
                units.append(e)
                unit_id += 1
            row.append(content)
        battleground.append(row)

    rounds = 0
    print(rounds)
    print_battleground(battleground, units)

    while len(elves) > 0 and len(goblins) > 0:
        temp_units = sorted(units, key=lambda x: (x.y, x.x))
        for unit in temp_units:
            if unit.dead:
                continue
            nearest_dist = None
            nearest_enemy = None
            attackable_enemies = []
            shortest_path = None
            if unit._type == 'goblin':
                _list = elves
            else:
                _list = goblins
            if not _list:
                break
            for enemy in _list:
                if (enemy.x, enemy.y) in ((unit.x + 1, unit.y), (unit.x - 1, unit.y), (unit.x, unit.y + 1), (unit.x, unit.y - 1)):
                    attackable_enemies.append(enemy)
                    nearest_dist = 1
                    continue
                path = distance(battleground, unit, enemy)
                if path is None:
                    continue
                path_len = len(path)
                if not nearest_dist or path_len < nearest_dist:
                    nearest_dist = path_len
                    nearest_enemy = enemy
                    shortest_path = path
                elif path_len == nearest_dist:
                    if enemy.y < nearest_enemy.y:
                        nearest_enemy = enemy
                        shortest_path = path
                    elif enemy.y == nearest_enemy.y:
                        if enemy.x <= nearest_enemy.x:
                            nearest_enemy = enemy
                            shortest_path = path
            if nearest_dist:
                if nearest_dist > 1:
                    print(f'moving {unit} from {shortest_path[0]} to {shortest_path[1]} with target {shortest_path[-1]}')
                    move(battleground, unit, shortest_path)
            for enemy in _list:
                if enemy in attackable_enemies:
                    continue
                if (enemy.x, enemy.y) in ((unit.x + 1, unit.y), (unit.x - 1, unit.y), (unit.x, unit.y + 1), (unit.x, unit.y - 1)):
                    attackable_enemies.append(enemy)
            if attackable_enemies:
                enemy = sorted(attackable_enemies, key=lambda x: (x.hp, x.y, x.x))[0]
                enemy.hp -= 3
                if enemy.hp <= 0:
                    kill_unit(enemy, _list, units, battleground)
                    print(f'killing unit {enemy}, killing blow: {unit} at {unit.y}, {unit.x}')
            if unit == temp_units[-1]:
                rounds += 1
        print(rounds)
        print_battleground(battleground, units)
    winners = ''
    total_hp = 0
    for x in elves + goblins:
        winners = x._type
        total_hp += x.hp
    print(winners, rounds, total_hp, total_hp * rounds)


_input = []
for line in sys.stdin.readlines():
    _input.append([x for x in line.strip()])
    width = len(_input[0])
    height = len(_input)


if __name__ == '__main__':
    main()
