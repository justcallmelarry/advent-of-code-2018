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


def bfs(grid, start, enemy):
    grid[enemy.y][enemy.x] = '*'
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == '*':
            # grid[enemy.y][enemy.x] = enemy
            grid[enemy.y][enemy.x] = enemy._name
            return path
        for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] in ('.', '*') and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
    grid[enemy.y][enemy.x] = enemy._name


def move(battleground, unit, enemy):
    path = bfs(battleground, (unit.x, unit.y), enemy)
    if path:
        battleground[unit.y][unit.x] = '.'
        unit.x, unit.y = path[1]
        battleground[unit.y][unit.x] = unit._name


def move2(battleground, unit, enemy):
    def calc_direction(direction, num1, num2):
        if num1 < num2:
            direction.append(1)
        elif num1 == num2:
            direction.append(0)
        elif num1 > num2:
            direction.append(-1)
    direction = []
    calc_direction(direction, unit.x, enemy.x)
    calc_direction(direction, unit.y, enemy.y)
    if direction[0] != 0 and battleground[unit.y][unit.x + direction[0]] == '.':
        battleground[unit.y][unit.x] = '.'
        unit.x += direction[0]
        battleground[unit.y][unit.x] = unit._name
    elif battleground[unit.y + direction[1]][unit.x] == '.':
        battleground[unit.y][unit.x] = '.'
        unit.y += direction[1]
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
    path = bfs(battleground, (unit.x, unit.y), enemy)
    return len(path) - 1 if path else None


def distance2(battleground, unit, enemy):  # saving for later
    possible_coords = [
        (unit.x - 1, unit.y),
        (unit.x + 1, unit.y),
        (unit.x, unit.y + 1),
        (unit.x, unit.y - 1)
    ]
    shortest_path = None
    for coords in possible_coords:
        if battleground[coords[1]:coords[0]] != '.':
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
    return len(shortest_path) if shortest_path else None, None


def print_battleground(battleground):
    for o in battleground:
        print(''.join(o))
    return
    s = [[str(e) for e in row] for row in battleground]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


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
    print_battleground(battleground)

    while len(elves) > 0 and len(goblins) > 0:
        for unit in sorted(units, key=lambda x: (x.y, x.x)):
            if unit.dead:
                continue
            nearest_dist = None
            nearest_enemy = None
            attackable_enemies = []
            if unit._type == 'goblin':
                _list = elves
            else:
                _list = goblins
            for enemy in _list:
                enemy_distance = distance(battleground, unit, enemy)
                if enemy_distance is None:
                    continue
                if enemy_distance == 1:
                    attackable_enemies.append(enemy)
                    nearest_dist = 1
                else:
                    if not nearest_dist or enemy_distance < nearest_dist:
                        nearest_dist = enemy_distance
                        nearest_enemy = enemy
                    elif enemy_distance == nearest_dist:
                        if enemy.y < nearest_enemy.y:
                            nearest_enemy = enemy
                        elif enemy.y == nearest_enemy.y:
                            if enemy.x <= nearest_enemy.x:
                                nearest_enemy = enemy
            if nearest_dist:
                if nearest_dist > 1:
                    move(battleground, unit, nearest_enemy)
                for enemy in _list:
                    enemy_distance = distance(battleground, unit, enemy)
                    if enemy_distance is None:
                        continue
                if enemy_distance == 1:
                    attackable_enemies.append(enemy)
                if attackable_enemies:
                    enemy = sorted(attackable_enemies, key=lambda x: x.hp)[0]
                    enemy.hp -= 3
                    if enemy.hp <= 0:
                        kill_unit(enemy, _list, units, battleground)
                        print(f'killing unit {enemy}, killing blow: {unit} at {unit.y}, {unit.x}')
        if not elves or not goblins:
            rounds -= 1
        rounds += 1
        print(rounds)
        print_battleground(battleground)
        print(units)
        print()
    winners = ''
    total_hp = 0
    for x in elves + goblins:
        winners = x._type
        total_hp += x.hp
    print(winners, total_hp, rounds, total_hp * rounds)


_input = []
for line in sys.stdin.readlines():
    _input.append([x for x in line.strip()])
    width = len(_input[0])
    height = len(_input)


if __name__ == '__main__':
    main()