#!/usr/bin/python3

# python3 -m doctest -v 06b.py

'''
--- Part Two ---

While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...
Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...
Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...
Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...
Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...
Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..
It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?
'''

import copy, sys

with open('input/06.txt', 'r') as f:
# with open('input/06-small.txt', 'r') as f:
    lines = f.readlines()
field = [l.rstrip() for l in lines]

dir = '^>v<'
dxdy = [(0, -1), (1, 0), (0, 1), (-1, 0)]
def find_pos():
    for y in range(len(field)):
        for x in range(len(field[0])):
            ch = field[y][x]
            if ch in dir:
                d = ch
                return (x, y, d)
    print('@@@@@@@@@@')
    print('Cannot find init pos')
    print('@@@@@@@@@@')
    sys.exit(3)

def is_valid(pos):
    x, y = pos
    return 0 <= x < len(field[0]) and 0 <= y < len(field)

init_x, init_y, initial_d = find_pos()
initial_pos = (init_x, init_y)
def traverse(field):
    pos = initial_pos
    d = initial_d
    visited = set() # (x, y, d)
    path = []
    while is_valid(pos) and not (pos[0], pos[1], d) in visited:
        x, y = pos
        visited.add( (x, y, d) )
        path.append((x, y, d))
        id = dir.find(d)
        dx, dy = dxdy[id]
        new_x, new_y = x + dx, y + dy
        new_pos = (new_x, new_y)
        if is_valid(new_pos):
            if field[new_y][new_x] != '.':
                new_pos = pos
                new_id = (id + 1) % len(dir)
                d = dir[new_id]
        pos = new_pos
    res = 0 if not is_valid(pos) else 1
    return (res, path)

def print_field(f):
    for s in f:
        print(s)

# remove initial pos so it does not block
field[init_y] = field[init_y][:init_x] + '.' + field[init_y][init_x+1:]

_, path = traverse(field)
cnt = 0

def apply_path(field, path):
    f = copy.deepcopy(field)
    for x, y, d in path:
        f[y] = f[y][:x] + d + f[y][x+1:]
    return f
# print_field(apply_path(field, path))

for y in range(len(field)):
    for x in range(len(field[0])):
        if not (x == initial_pos[0] and y == initial_pos[1]):
            f = copy.deepcopy(field)
            f[y] = field[y][:x] + 'O' + field[y][x+1:]
            res, path = traverse(f)
            if res > 0:
                cnt += 1
                # print_field(apply_path(f, path))
                # print('@@@@@@@@@@')

print('===============================')
print('The answer: ', cnt)
print('===============================')
